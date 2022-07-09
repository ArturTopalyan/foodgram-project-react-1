from django.apps import apps
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Recipe
from .serializers import RecipeShortInfo


def sub_action(request: Request, model_name: str, pk: int):
    """
    Данный метод обрабатывает однотипные запросы.

    :param request: объект типа rest_framework.request.Request
    :param model_name: строка, определяющая вспомогательную модель.
    Соответствует шаблону <app_lable>.<model_name>
    :param pk: id рецепта

    Метод создает, или удаляет, в зависимости от типа запроса вспомогательную
    модель model_name с пользователем, отправившим запрос и recipe с id id.
    Примеры вспомогательной модели - Follow, или Cart
    """

    model = apps.get_model(model_name)
    if pk is None or not Recipe.objects.filter(id=pk).exists():
        return Response(
            {'error': 'recipe object with id %s doesn\'t exists' % pk},
            status=status.HTTP_400_BAD_REQUEST,
        )
    recipe = Recipe.objects.get(id=pk)
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
