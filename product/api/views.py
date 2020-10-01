from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from commenting.api.serializers import CommentingSerializer
from commenting.models import ProductComment
from product.api.serializers import CategorySerializer, ProductSerializer, BookmarkSerializer, RateSerializer
from product.filter import CistomOrdering
from product.models import Category, Product
from product.pagination import CustiomLimitOffsetPagination, CustomPageNumberPagination


class InitialView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"test": "helloo"})

    def post(self, request, *args, **kwargs):
        data = request.data
        return Response(data)


class CategoryViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    pagination_class = CustomPageNumberPagination
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(is_enable=True).all()

    # lookup_url_kwarg = 'id'

    # def retrieve(self, request, *args, **kwargs):
    #     category = self.get_object()
    #     related_products = Product.objects.filter(categurise=category)
    #     serializer = ProductSerializer(related_products,many=True)
    #     return Response(serializer.data)

    # def create_return(self, query):
    #     dict_temp = {}
    #     dict_temp["id"] = query.id
    #     dict_temp["created_time"] = query.created_time
    #     dict_temp["name"] = query.name
    #     next_query = Category.objects.filter(parent=query.id)
    #     if list(next_query.values()) != []:
    #         list_temp = []
    #         for q in next_query:
    #             list_temp.append(self.create_return(q))
    #         dict_temp["child"] = list_temp
    #     return dict_temp
    @method_decorator(cache_page(20))
    def list(self, request, *args, **kwargs):
        # return_data = []
        # for i in self.queryset.filter(parent__isnull=True):
        #     return_data.append(self.create_return(i))
        # return Response(return_data)
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        query = self.queryset.filter(parent__isnull=True)
        serializer = CategorySerializer(query, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        category = self.get_object()
        products_properties = {}
        for p in category.properties:
            products_properties[p] = Product.objects.filter(
                categurise=category).values_list(f'properties__{p}', flat=True).distinct()
        return Response(products_properties)


class ProductViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, CistomOrdering, SearchFilter, ]
    pagination_class = CustiomLimitOffsetPagination
    search_fields = ['name', 'categurise__name']
    ordering_fields = ['id', 'name', 'rating_avg', 'rating_count']
    # filter_fields = ['id', 'categurise']
    filter_fields = {'price': ['lt', 'gt'], 'categurise__id': ['in', ]}
    queryset = Product.objects.filter(is_enable=True)

    def get_serializer_class(self):
        serializer_class = {
            "bookmark": BookmarkSerializer,
            "rate": RateSerializer,
            "add_comment": CommentingSerializer
        }
        return serializer_class.get(self.action) or super().get_serializer_class()

    @action(methods=['post'], detail=True)
    def bookmark(self, request, *args, **kwargs):
        user = request.user
        product = self.get_object()
        serializer = BookmarkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, product=product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True)
    def rate(self, request, *args, **kwargs):
        user = request.user
        product = self.get_object()
        serializer = RateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, product=product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True, url_path="add-comment")
    def add_comment(self, request, *args, **kwargs):
        user = request.user
        product = self.get_object()
        serializer = CommentingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, product=product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True)
    def comments(self, request, *args, **kwargs):
        product = self.get_object()
        related_comments = ProductComment.approves.filter(product=product)
        serializer = CommentingSerializer(related_comments, many=True)
        return Response(serializer.data)
