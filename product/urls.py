from django.urls import path, include

from product.views import product_detail_view, products_list, stores_list, create_product, ProductListViwe, \
    ProductDetailView, ProductCreateView, ProductUpdateView, RateView, RateDeleteView, CategoryListView, \
    CategoryDetailView, BookMarkcreateView

urlpatterns = [

    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('<int:pk>/bookmark', BookMarkcreateView.as_view(), name='bookmark'),
    #path('', products_list, name='products-list'),
    path('', ProductListViwe.as_view(), name='products-list'),
    path('create-product/', ProductCreateView.as_view(), name='create-product'),
    path('<int:pk>/update', ProductUpdateView.as_view(), name='product-update'),
    path('<int:pk>/rate', RateView.as_view(), name='rate'),
    path('<int:pk>/rate-delete', RateDeleteView.as_view(), name='product-rate-delete'),
    path('stores/', stores_list, name='stores-list'),
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/<int:pk>/category_detail', CategoryDetailView.as_view(), name='category_detail'),


    #API
    path('api/', include("product.api.urls"))
]