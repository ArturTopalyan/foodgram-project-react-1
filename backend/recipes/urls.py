from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientsViewSet, RecipeViewSet

router = DefaultRouter()

router.register(
    r'^ingredients',
    IngredientsViewSet,
)
router.register(
    r'^recipes',
    RecipeViewSet,
)

urlpatterns = [
    path('', include(router.urls)),
]
