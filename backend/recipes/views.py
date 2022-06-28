from django.http.response import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .filters import IngredientFilter, RecipeFilter
from .models import Cart, Ingredient, Recipe
from .permissions import AuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipeCreateSerializer,
                          RecipeGetSerializer, RecipeShortInfo)


class IngredientsViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filter_class = IngredientFilter


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (AuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method not in SAFE_METHODS:
            return RecipeCreateSerializer
        return RecipeGetSerializer

    @action(
        path='shopping_cart',
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,),
    )
    def shopping_cart(self, request, id=None):
        if id is None or not Recipe.objects.filter(id=id).exists():
            return Response(
                {'error': 'recipe object with id %s doesn\'t exists' % id},
                status=status.HTTP_400_BAD_REQUEST,
            )
        recipe = Recipe.objects.get(id=id)
        kwargs = {
            'user': request.user,
            'recipe': recipe,
        }
        if request.method == 'post':
            Cart.objects.create(
                **kwargs,
            )
            return Response(
                RecipeShortInfo(recipe, many=False),
                status=status.HTTP_201_CREATED,
            )
        Cart.objects.delete(
            **kwargs,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        path='download_shopping_cart',
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,),
    )
    def download_shopping_cart(self, request):
        recipes = request.user.recipes.all()
        shopping_list = {}
        for ingredient in recipes.ingredients.all():
            name = ingredient.ingredient.name
            amount = ingredient.amount
            measurement_unit = ingredient.measurement_unit
            if name in shopping_list:
                shopping_list[name]['amount'] += amount
            else:
                shopping_list[name] = {
                    'amount': amount,
                    'measurement_unit': measurement_unit,
                }
        cart = [
            '%(name)s %(amount)s %(measurement_unit)s\n' % {
                'name': name,
                'amount': data['amount'],
                'measurement_unit': data['measurement_unit'],
            } for name, data in shopping_list.items()
        ]
        response = HttpResponse(
            cart,
            'Content-Type: text/plain',
        )
        response['Content-Disposition'] = (
            'attachment; filename="shopping_cart.txt"'
        )
        return response
