import base64
import uuid

from django.core.files.base import ContentFile
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ImageField

ALLOWED_IMAGE_TYPES = (
    'jpeg',
    'jpg',
    'png',
    'gif'
)


class Base64ImageField(ImageField):
    def to_internal_value(self, base64_data):
        data = str(base64_data).split(',')
        base64_data = data[-1]
        if base64_data is None or len(base64_data) == 0:
            return None
        try:
            decoded_file = base64.b64decode(base64_data)
        except TypeError:
            raise ValidationError('Неправильное изображение.')
        file_name = str(uuid.uuid4())[:12]
        # data string is like 'data:image/png;base64,data...'
        file = data[0].split(':')[-1].split(';')[0]
        # file variable is like 'image/png'
        file_type, file_extension = file.split('/')
        if file_type != 'image':
            raise ValidationError(
                'Это не изображение'
            )
        if file_extension not in ALLOWED_IMAGE_TYPES:
            raise ValidationError(
                'Неправильный формат изображения.'
            )
        complete_file_name = file_name + '.' + file_extension
        data = ContentFile(decoded_file, name=complete_file_name)
        return super(Base64ImageField, self).to_internal_value(data)

    def to_representation(self, value):
        return value.name
