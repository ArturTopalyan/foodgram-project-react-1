from django.core.validators import RegexValidator


class HexColorValidator(RegexValidator):
    regex = r'^#[A-F0-9]{6}$'
    message = (
        'Color must be as represented as HEX num'
        '(only letters A-F and digits 0-9).'
    )


class SlugValidator(RegexValidator):
    regex = r'^[\w]+$',
    message = 'Введите корректный slug'
