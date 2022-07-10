from django.contrib.auth import authenticate
from django.http import HttpResponse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import LoginSerializer, RegisterSerializer


def index(request):
    return HttpResponse("JNNSDANDAS")


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
