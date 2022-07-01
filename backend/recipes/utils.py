from django.apps import apps


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

    model = apps.get_model(related_class)
    if request is None or request.user.is_anonymous:
        return False
    kwargs[user_field or 'user'] = request.user
    return model.objects.filter(
        **kwargs,
    ).exists()
