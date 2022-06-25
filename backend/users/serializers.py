from rest_framework import serializers

from .models import User


class UserGetSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )
        model = User

    def get_is_subscibed(self, obj: User):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return User.objects.filter(
            user=request.user,
            author__id=obj.id,
        ).exists()


class UserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
        )
        model = User

    def validate(self, attrs):
        return super().validate(attrs)
