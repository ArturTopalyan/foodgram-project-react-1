from django.core.validators import RegexValidator


class SlugValidator(RegexValidator):
    regex = r'^[\w]+$',
    message = 'Введите корректный slug'
