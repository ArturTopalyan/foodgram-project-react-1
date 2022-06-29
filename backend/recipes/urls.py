from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GetSubscriptionsViewSet, IngredientsViewSet, RecipeViewSet

router = DefaultRouter()

router.register(
    r'^ingredients',
    IngredientsViewSet,
)
router.register(
    r'^recipes',
    RecipeViewSet,
)
router.register(
    r'^users/subscriptions',
    GetSubscriptionsViewSet,
    'get_user_subscriptions',
)

urlpatterns = [
    path('', include(router.urls)),
]
