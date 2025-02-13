from django.contrib.auth.models import get_user_model
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'password', 'nickname', 'roles')
        extra_kwargs = {
            'roles': {'read_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
