from importlib.metadata import requires
from re import search
from urllib import request
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["username"],
            validated_data["email"],
            validated_data["password"],
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)


class ProfileSerializer(serializers.Serializer):
    user = serializers.CharField()
    bio = serializers.CharField()
    institution = serializers.CharField()
    correct_submissions = serializers.IntegerField()
    incorrect_submissions = serializers.IntegerField()
    runtime_error_submissions = serializers.IntegerField()
