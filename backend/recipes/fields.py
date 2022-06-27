from base64 import urlsafe_b64encode

from rest_framework.fields import Field


class ImageToB64(Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        return urlsafe_b64encode(data)
