from django.urls import path, include
from rest_framework.routers import SimpleRouter

from product.api.serializers import CategorySerializer, ProductSerializer
from product.api.views import InitialView, CategoryViewSet, ProductViewSet



router = SimpleRouter()

router.register('category-api', CategoryViewSet)
router.register('product-api', ProductViewSet)

urlpatterns = [

    path('', InitialView.as_view(), name="initial"),
    path('', include(router.urls), name="product-roter"),

    # path('category-api/', CategoryViewSet.as_view({'get': 'list'}), name="categories-api"),
    # path('category-api/<int:pk>', CategoryViewSet.as_view({'get': 'retrieve'}), name="categories-api"),
    # path('product-api/', ProductViewSet.as_view({'get': 'list'}), name="product-api"),
    # path('product-api/<int:pk>', ProductViewSet.as_view({'get': 'retrieve'}), name="product-api"),
]
