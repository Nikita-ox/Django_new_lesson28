from rest_framework import serializers

from authentication.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = super().create(validated_data)
        '''сохраняем пользователя так как он есть'''

        user.set_password(user.password)
        '''переопределим пароль, hash'''
        user.save()

        return user

