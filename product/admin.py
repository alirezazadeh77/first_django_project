from django.contrib import admin
from django import forms
from prettyjson import PrettyJSONWidget

from .models import Product, ProductRating, Category, ProductBookMark
from .models import Store


# Register your models here.
# admin.site.register(Product)
# admin.site.register(Store)
# admin.site.register(ProductRating)
# admin.site.register(Category)
# admin.site.register(ProductBookMark)

class CateforyForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {'properties': PrettyJSONWidget()}


@admin.register(Category)
class CtegoriesAdmin(admin.ModelAdmin):
    form = CateforyForm
    list_display = ["name", "parent", "is_enable"]
    list_filter = ["is_enable", ]
    raw_id_fields = ["parent", ]
    search_fields = ["name", ]
    actions = ['set_enable', 'set_disable']

    def set_enable(self, request, queryset):
        queryset.filter(is_enable=False).update(is_enable=True)

    def set_disable(self, request, queryset):
        queryset.filter(is_enable=True).update(is_enable=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_filter = ["is_enable", ]
    list_display = ["name", "price", "is_enable"]
    autocomplete_fields = ["categurise"]
    search_fields = ['name']
