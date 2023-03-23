from rest_framework import serializers
from django.contrib.auth import authenticate, login
from user.models import UserModel


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["id", "first_name", "last_name", "username", "password", "email"]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return UserModel.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, write_only=True)
    password = serializers.CharField(max_length=100, write_only=True)

    def create(self, validated_data):
        user = authenticate(username=validated_data['username'], password=validated_data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        login(self.context.get('request'), user)
        return user
