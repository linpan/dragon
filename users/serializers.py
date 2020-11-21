from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


class RegisterUserSerializer(serializers.ModelSerializer):
    """Serializer for creating user objects."""

    password = serializers.CharField(
        min_length=8,
        write_only=True
    )
    re_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 're_password', 'email')

    def create(self, validated_data):
        password = validated_data.get("password")
        re_password = validated_data.get("re_password")
        email = validated_data.get("email")

        if re_password != password:
            raise ValidationError("两次密码输入不一致")

        if User.objects.filter(email=email):
            raise ValidationError("邮箱已被注册")

        validated_data.pop('re_password')
        user = User.objects.create_user(**validated_data)
        return user