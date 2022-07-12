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
    tle_submissions = serializers.IntegerField()


class BlogListSerializer(serializers.Serializer):
    id = serializers.CharField()
    author = serializers.CharField()
    name = serializers.CharField()
    date = serializers.DateField()
    timestamp = serializers.TimeField()


class BlogSerializer(serializers.Serializer):
    id = serializers.CharField()
    author = serializers.CharField()
    name = serializers.CharField()
    statement = serializers.CharField()
    date = serializers.DateField()
    timestamp = serializers.TimeField()


class QuestionsListSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()


class QuestionSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    statement = serializers.CharField()
    timelimit = serializers.CharField()
    memlimit = serializers.CharField()
    tags = serializers.ManyRelatedField(id)


class SubmissionDataSerializer(serializers.Serializer):
    id = serializers.CharField()
    user = serializers.CharField()
    ques = serializers.CharField()
    code = serializers.CharField()
    lang = serializers.CharField()
    verdict = serializers.CharField()


class SubmissionSerializer(serializers.Serializer):
    ques = serializers.CharField()
    code = serializers.CharField()
    lang = serializers.CharField()

    def validate(self, data):
        ques = data["ques"]
        lang = data["lang"]
        if Question.objects.filter(id=ques).count() == 0:
            raise serializers.ValidationError("Question Id is invalid")
        if lang not in ["c++", "python", "java"]:
            raise serializers.ValidationError(
                "Language not supported, supported languages include: 'c++', 'java' and 'python'"
            )
        return data
