from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientsViewSet

router = DefaultRouter()

router.register(
    r'^ingredients',
    IngredientsViewSet,
)

urlpatterns = [
    path('', include(router.urls)),
]
