from django.contrib.auth import authenticate
from django.http import HttpResponse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import *

from .serializers import LoginSerializer, ProfileSerializer, RegisterSerializer


def index(request):
    return HttpResponse(
        "<h1>This is an API only Application, Please access the <a href='http://localhost:1338'>frontend client</a> <h1>"
    )


# Register API
@api_view(["POST"])
def registerAPI(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    return Response(
        {
            "message": "success",
            "user": LoginSerializer(user).data,
            "token": Token.objects.get_or_create(user=user)[0].key,
        }
    )


@api_view(["POST"])
def loginAPI(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data["username"]
    password = serializer.validated_data["password"]
    user = authenticate(username=username, password=password)
    if user:
        return Response(
            {
                "message": "success",
                "user": LoginSerializer(user).data,
                "token": Token.objects.get_or_create(user=user)[0].key,
            }
        )
    else:
        return Response(
            {
                "message": "error",
                "error": "Invalid Username/Password",
            }
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logoutAPI(request):
    try:
        request.user.auth_token.delete()
    except:
        pass
    return Response(
        {
            "message": "success",
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profileAPI(request):
    user = request.user
    user_profile = Profile.objects.get_or_create(user=user)[0]
    return Response(
        {
            "message": "success",
            "profile_data": ProfileSerializer(user_profile).data,
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def blogsAPI(request, blogId=1):
    user = request.user
    user_profile = Profile.objects.get_or_create(user=user)
    return Response(
        {
            "message": "success",
            "profile_data": ProfileSerializer(user_profile).data,
        }
    )
