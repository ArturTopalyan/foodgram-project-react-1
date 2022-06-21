from django.core.validators import RegexValidator


class HexColorValidator(RegexValidator):
    regex = r'^#[ABCDEF\d]{6}$'
    message = (
        'Color must be as represented as HEX num'
        '(only letters A-F and digits 0-9).'
    )
