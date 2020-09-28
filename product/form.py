from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from product.models import Product, ProductRating, ProductBookMark


class RateForm(forms.ModelForm):
    class Meta:
        model = ProductRating
        fields = ['rate', ]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'categurise', 'image']

    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "name..."}))
    price = forms.CharField(widget=forms.NumberInput(attrs={"placeholder": "price"}))
    description = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "something...."}))
    image = forms.ImageField()
    categurise = forms.SelectMultiple()


class RawProductForm(forms.Form):
    name = forms.CharField()
    price = forms.IntegerField(initial=10)
    # description = forms.CharField(required=False,label="DD",help_text="plese enter some description")
    description = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "something...."}))


class SearchForm(forms.Form):
    value = forms.CharField(widget=forms.TextInput())
    categuiry_check = forms.CheckboxInput()
    product_check = forms.CheckboxInput()


class BookMarkForm(forms.ModelForm):
    class Meta:
        model = ProductBookMark
        fields = ["like_status", ]


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=50, required=False, help_text='Optional')
    email = forms.EmailField(max_length=254, help_text='enter a valid email address')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
