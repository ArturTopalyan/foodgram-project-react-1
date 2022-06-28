from django.apps import apps
from rest_framework import status
from rest_framework.response import Response

from .models import Recipe
from .serializers import RecipeShortInfo


def get_sub_exist(
    request,
    related_class: str,
    user_field: None | str = None,
    **kwargs
) -> bool:
    """
    :param request: объект класса request
    :param related_class str: связанный класс по шаблону
    <app_lable>.<model_name>
    :param user_field:
    Данная функция поможет определить, существует ли объект класса
    related_class с пользователем, который отправляет запрос.
    Используется как дополнение для SerializerMethodField
    request, obj надо просто передать из функции, к которой привязано поле
    SerializerMethodField.
    related_class - строка, определяющая модель, соответствует шаблону
    <app_lable>.<model_name>.
    Например,если модель Recipe приложения recipes, то на вход надо передать
    строку 'recipes.Recipe'
    """

    app_lable, model_name = related_class.split('.')
    model = apps.get_model(app_label=app_lable, model_name=model_name)
    if request is None or request.user.is_anonymous:
        return False
    kwargs[user_field or 'user'] = request.user
    return model.objects.filter(
        **kwargs,
    ).exists()


def sub_action(request, model_name, id):
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
