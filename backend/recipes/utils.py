from django.apps import apps


def get_sub_exist(request, sub: str, user_field=None, **kwargs):
    """
    Данная функция поможет определить, существует ли объект класса sub
    с пользователем, который отправляет запрос.
    Используется как дополнение для SerializerMethodField
    request, obj надо просто передать из функции, к которой привязано поле
    SerializerMethodField.
    sub - строка, определяющая модель. Например,если модель Recipe приложения
    recipes, то на вход надо передать строку шаблона "<app_lable>.<model_name>"
    Тоесть 'recipes.Recipe'.
    """

    app_lable, model_name = sub.split('.')
    model = apps.get_model(app_label=app_lable, model_name=model_name)
    if request is None or request.user.is_anonymous:
        return False
    if user_field is None:
        user_field = 'user'
    kwargs[user_field] = request.user
    return model.objects.filter(
        **kwargs,
    ).exists()
