from django.contrib.auth import authenticate
from django.http import HttpResponse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .tasks import compile_and_run, test

from .models import *

from .serializers import (
    BlogSerializer,
    BlogListSerializer,
    LoginSerializer,
    ProfileSerializer,
    QuestionSerializer,
    QuestionsListSerializer,
    RegisterSerializer,
    SubmissionDataSerializer,
    SubmissionSerializer,
)


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
            "detail": "success",
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
                "detail": "success",
                "user": LoginSerializer(user).data,
                "token": Token.objects.get_or_create(user=user)[0].key,
            }
        )
    else:
        return Response(
            {
                "detail": "error",
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
            "detail": "success",
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profileAPI(request):
    user = request.user
    user_profile = Profile.objects.get_or_create(user=user)[0]
    return Response(
        {
            "detail": "success",
            "profile_data": ProfileSerializer(user_profile).data,
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def blogsAPI(request):
    blogs_queryset = Blog.objects.all()
    blogs_data = BlogListSerializer(blogs_queryset, many=True).data
    return Response(
        {
            "detail": "success",
            "blogs_data": blogs_data,
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getBlogAPI(request, blogId):
    try:
        blog_query_object = Blog.objects.get(id=blogId)
        return Response(
            {
                "detail": "success",
                "blog_data": BlogSerializer(blog_query_object).data,
            }
        )
    except:
        return Response(
            {
                "detail": "error",
                "blog_data": "Invalid Blog ID",
            }
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def questionsAPI(request):
    questions_queryset = Question.objects.all()
    questions_data = QuestionsListSerializer(questions_queryset, many=True).data
    return Response(
        {
            "detail": "success",
            "blogs_data": questions_data,
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getQuestionAPI(request, questionId):
    try:
        print(questionId)
        question_query_object = Question.objects.get(id=questionId)
        return Response(
            {
                "detail": "success",
                "blog_data": QuestionSerializer(question_query_object).data,
            }
        )
    except Exception as e:
        print(e)
        return Response(
            {
                "detail": "error",
                "blog_data": "Invalid Question ID",
            }
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def submitAPI(request):
    submission_data = SubmissionSerializer(data=request.data)
    submission_data.is_valid(raise_exception=True)
    ques = submission_data.validated_data["ques"]
    code = submission_data.validated_data["code"]
    lang = submission_data.validated_data["lang"]
    submission = Submission(
        user=User.objects.get(username=request.user),
        ques=Question.objects.get(id=ques),
        code=code,
        lang=lang,
    )
    submission.save()
    submission_obj = SubmissionDataSerializer(submission).data
    return Response(
        {
            "detail": "success",
            "blog_data": "Submitted",
            "submission_data": submission_obj,
        }
    )
