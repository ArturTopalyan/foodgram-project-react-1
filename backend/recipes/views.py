from django.apps import apps
from django.http.response import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import (GenericViewSet, ModelViewSet,
                                     ReadOnlyModelViewSet)

from .filters import IngredientFilter, RecipeFilter
from .models import Ingredient, Recipe
from .permissions import AuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipeCreateSerializer,
                          RecipeGetSerializer, RecipeShortInfo,
                          UserInSubscriptionsSerializer)


def sub_action(request: Request, model_name: str, id: int):
    """
    Данный метод обрабатывает однотипные запросы.

    :param request: объект типа rest_framework.request.Request
    :param model_name: строка, определяющая вспомогательную модель.
    Соответствует шаблону <app_lable>.<model_name>
    :param id: id рецепта

    Метод создает, или удаляет, в зависимости от типа запроса вспомогательную
    модель model_name с пользователем, отправившим запрос и recipe с id id.
    Примеры вспомогательной модели - Follow, или Cart
    """

    model = apps.get_model(model_name)
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
    if request.method.lower() == 'delete':
        model.objects.get(
            **kwargs,
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    model.objects.get_or_create(
        **kwargs,
    )
    return Response(
        RecipeShortInfo(recipe, many=False).data,
        status=status.HTTP_201_CREATED,
    )


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
        carts = request.user.carts.all()
        shopping_list = {}
        for cart in carts:
            recipe = cart.recipe
            for ingredient_recipe in recipe.ingridients_in_recipe.all():
                name = ingredient_recipe.ingredient.name
                amount = ingredient_recipe.amount
                meas_unit = ingredient_recipe.ingredient.measurement_unit
                if name in shopping_list:
                    shopping_list[name]['amount'] += amount
                else:
                    shopping_list[name] = {
                        'amount': amount,
                        'measurement_unit': meas_unit,
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


class GetSubscriptionsViewSet(ListModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserInSubscriptionsSerializer

    def get_queryset(self):
        return list(
            map(
                lambda follow: follow.author,
                self.request.user.following.all()
            )
        )
