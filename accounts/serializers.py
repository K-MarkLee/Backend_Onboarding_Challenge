from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'nickname', 'roles')
        extra_kwargs = {
            'password': {'write_only': True},
            'roles': {'read_only': True}
        }


    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
