from django.urls import path, include
from rest_framework.routers import SimpleRouter

from commenting.api.views import CommetingVewsSet

router = SimpleRouter()
router.register('', CommetingVewsSet)

urlpatterns = [

    path('', include(router.urls), name="initial"),

]
