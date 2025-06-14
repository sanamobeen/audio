from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class SignInSerializer(serializers.Serializer):
    class Meta:
        model = User

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError as e:
            raise serializers.ValidationError({"refresh": "Invalid or expired token"})
