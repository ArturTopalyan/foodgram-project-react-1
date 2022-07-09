from django.contrib.auth import get_user_model
from django.http.response import HttpResponse
from django.db.models.aggregates import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.viewsets import (GenericViewSet, ModelViewSet,
                                     ReadOnlyModelViewSet)

from .filters import IngredientFilter, RecipeFilter
from .local_utils import sub_action
from .models import Ingredient, Recipe, IngridientInRecipe
from .permissions import AuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipeCreateSerializer,
                          RecipeGetSerializer, UserInSubscriptionsSerializer)

User = get_user_model()


class IngredientsViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (AuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeGetSerializer
        return RecipeCreateSerializer

    @action(
        url_path='shopping_cart',
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,),
    )
    def shopping_cart(self, request, id=None):
        return sub_action(request, 'recipes.Cart', id)

    @action(
        url_path='favorite',
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,),
    )
    def favorite_recipe(self, request, id=None):
        return sub_action(request, 'recipes.Favorite', id)

    @action(
        url_path='download_shopping_cart',
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,),
    )
    def download_shopping_cart(self, request):
        shopping_list = IngridientInRecipe.objects.filter(
            recipe__carts__user=request.user,
        ).values(   # returns list or dicts like [{'ingredient__name': ...},.]
            'ingredient__name',
            'ingredient__measurement_unit',
        ).annotate(amount=Sum('amount'))
        cart = [
            '%(name)s %(amount)s %(measurement_unit)s\n' % {
                'name': data['ingredient__name'],
                'amount': data['amount'],
                'measurement_unit': data['ingredient__measurement_unit'],
            } for data in shopping_list
        ]
        response = HttpResponse(
            cart,
            'Content-Type: text/plain',
        )
        response['Content-Disposition'] = (
            'attachment; filename="shopping_cart.txt"'
        )
        return response


class GetSubscriptionsViewSet(ListModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserInSubscriptionsSerializer

    def get_queryset(self):
        return User.objects.filter(followers__user=self.request.user)
