from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, LoginView
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.context_processors import csrf
from django.urls import reverse, reverse_lazy
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.decorators import decorator_from_middleware, method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import ModelFormMixin

from product.form import ProductForm, RawProductForm, RateForm, BookMarkForm, SignUpForm
from product.models import Product, Store, ProductRating, Category, Screenes, ProductBookMark


def home(request):
    return render(request, 'base.html')


def product_detail_view(request, pk):
    # product_obj = Product.objects.get(pk=pk)
    product_obj = get_object_or_404(Product, pk=pk)
    try:
        product_obj = Product.objects.get(pk=pk)
    except Product.MultipleObjectsReturned:
        raise

    context = {'obj': product_obj}

    return render(request, 'products/product_detail.html', context=context)


def products_list(request):
    try:
        price_lte = request.GET['name']
    except:
        price_lte = ''
    queryset = Product.objects.is_enable()
    context = {'object_list': queryset, 'PostPrametr': price_lte}

    return render(request, 'products/products_list.html', context)


def stores_list(request):
    queryset = Store.objects.all()

    context = {'stores': queryset}

    return render(request, 'products/stores_list.html', context)


def create_product(request):
    form = ProductForm(request.POST or None)
    # form = RawProductForm(request.POST or None)
    if form.is_valid():
        # Product.objects.create(**form.cleaned_data)
        form.save()
    context = {'form': form}

    return render(request, 'products/create_product.html', context=context)


class ProductListViwe(ListView):
    queryset = Product.objects.all()
    template_name = "products/products_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['PostPrametr'] = 'ali'
        context['authenticated'] = self.request.user and self.request.user.is_authenticated
        return context


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    model = Product
    template_name = 'products/product_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['authenticated'] = self.request.user and self.request.user.is_authenticated
        user = self.request.user
        if user and user.is_authenticated:
            product = self.get_object()
            context["bookmark"] = False
            try:
                context["bookmark"] = ProductBookMark.objects.get(user=user, product=product).like_status
            except ProductBookMark.DoesNotExist:
                pass
        return context


class ProductCreateView(CreateView):
    template_name = "products/create_product.html"
    form_class = ProductForm
    model = Product

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['authenticated'] = self.request.user and self.request.user.is_authenticated
        return context


class ProductUpdateView(UpdateView):
    template_name = "products/create_product.html"
    form_class = ProductForm
    model = Product

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['authenticated'] = self.request.user and self.request.user.is_authenticated
        return context


class RateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy("login")
    model = ProductRating
    form_class = RateForm
    template_name = "products/product_rate_create.html"

    def get_success_url(self):
        return reverse("products-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = get_object_or_404(Product, id=self.kwargs.get('pk'))
        context['authenticated'] = self.request.user and self.request.user.is_authenticated

        return context

    def form_valid(self, form):
        user = self.request.user
        product = self.get_context_data()['product']
        ProductRating.objects.update_or_create(
            user=user,
            product=product,
            defaults={
                "rate":
                    form.cleaned_data["rate"]
            }
        )
        return HttpResponseRedirect(self.get_success_url())


class RateDeleteView(LoginRequiredMixin, DeleteView):
    model = ProductRating
    login_url = reverse_lazy("login")
    template_name = "products/product_rate_delete.html"

    def delete(self, request, *args, **kwargs):
        obj = get_object_or_404(ProductRating, **{'user': self.request.user, 'id': self.kwargs.get('pk')})
        obj.delete()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("products-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['authenticated'] = self.request.user and self.request.user.is_authenticated
        return context


class CategoryListView(ListView):
    model = Category
    template_name = "products/category_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['authenticated'] = self.request.user and self.request.user.is_authenticated
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = "products/category_detail.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['authenticated'] = self.request.user and self.request.user.is_authenticated
        products_proprties = {}
        category = self.get_object()
        for p in category.properties:
            products_proprties[p] = category.products.values_list(f'properties__{p}', flat=True)
        context['properties'] = products_proprties
        return context


class WellcomeScreen(ListView):
    template_name = "products/wellcome_screen.html"
    model = Screenes

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.search_request = None
        self.request_first = None
        self.product_search = None
        self.category_search = None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['products'] = None
        context['categories'] = None
        if self.search_request is not None:
            if self.product_search == "on":
                context['products'] = Product.objects.filter(name=self.search_request)
            if self.category_search == "on":
                context['categories'] = Category.objects.filter(name=self.search_request)
        context['authenticated'] = self.request.user and self.request.user.is_authenticated
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.GET != {}:
            try:
                self.product_search = request.GET["search_in_product"]
            except MultiValueDictKeyError:
                self.product_search = "off"
            try:
                self.category_search = request.GET["search_in_category"]
            except MultiValueDictKeyError:
                self.category_search = "off"
            self.search_request = request.GET["search_input"]

        return self.get(request, *args, **kwargs)


class CostumLogout(LogoutView):
    # next_page = reverse_lazy("login")
    def get_next_page(self):
        return reverse("login")


class CostumLogin(LoginView):
    template_name = "products/login.html"

    def get_success_url(self):
        return reverse("products-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['authenticated'] = self.request.user and self.request.user.is_authenticated
        return context


class BookMarkcreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy("login")
    form_class = BookMarkForm
    model = ProductBookMark
    template_name = "products/create_bookmark.html"

    def get_success_url(self):
        return reverse("product-detail", kwargs={'pk': self.kwargs.get('pk')})

    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        user = self.request.user
        ProductBookMark.objects.update_or_create(
            user=user,
            product=product,
            defaults={
                "like_status":
                    form.cleaned_data["like_status"]}
        )
        return HttpResponseRedirect(self.get_success_url())


class SingUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('products-list')
    template_name = 'products/signup.html'
