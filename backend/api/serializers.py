from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer
from rest_framework.fields import SerializerMethodField


User = get_user_model()


class UserGetSerializer(ModelSerializer):
    is_subscribed = SerializerMethodField()
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )
    
    def get_is_subscribed(self):
        return 'true'
