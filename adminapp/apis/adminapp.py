import sys
import requests
import traceback
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import authentication, permissions
from rest_framework.authentication import SessionAuthentication
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model, authenticate, logout, login
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import transaction
from adminapp.models import CustomUser, UserType, Post
from django.shortcuts import render, redirect
from rest_framework.permissions import IsAuthenticated

from ..serializers import (
    CreateAdminUserSerializer,
    CreatePostSerializer,
    UploadImageSerializer,
    PostListSerializer,
)

from ..services import (
    create_admin_user,
    create_post,
    upload_image,
)


class RegisterAPI(APIView):
    """API for creating User"""

    authentication_classes = [SessionAuthentication]

    def post(self, request):
        try:
            serializer = CreateAdminUserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                create_admin_user(**serializer.validated_data)
            return Response(status=status.HTTP_201_CREATED, data=_("User created succesfully."))
        except ValidationError as e:
            mes = "\n".join(e.messages)
            raise ValidationError(mes)
        except Exception:
            error_info = "\n".join(traceback.format_exception(*sys.exc_info()))
            print(error_info)
            data = {
                "Success": False,
                "msg": "User Registration Failed",
            }
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data)


class LoginAPI(APIView):
    """API for Admin Login."""

    authentication_classes = [SessionAuthentication]

    def post(self, request):
        serializer = CreateAdminUserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.user_type == UserType.ADMIN:
                # Login successful, return user data
                login(request, user)
                data = {
                   "Success": True,
                   "msg": "Login Success",
                }
                # return Response(status=status.HTTP_201_CREATED, data=data)
                return redirect("adminapp:post_list") 
            else:
            # Login failed
                return Response({'error': 'Invalid login credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # Invalid data
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)            


class LogOutAPI(APIView):
    """API for Logout."""
    def get(self, request):
        logout(request)
        return redirect("adminapp:login")            


class CreatePostAPI(APIView):
    """API for creating post for Admin"""

    authentication_classes = [SessionAuthentication]

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        try:
            serializer = CreatePostSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                create_post(user=user, **serializer.validated_data)
                data = {
                    "Success": True,
                    "msg": "New post created.",
                }
            return Response(status=status.HTTP_200_OK, data=data)
        except ValidationError as e:
            mes = "\n".join(e.messages)
            raise ValidationError(mes)
        except Exception:
            error_info = "\n".join(traceback.format_exception(*sys.exc_info()))
            print(error_info)
            data = {
                "Success": False,
                "msg": "Creating post failed",
            }
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data)


class UploadImageAPI(APIView):
    """API for upoading images for posts"""

    authentication_classes = [SessionAuthentication]

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        try:
            serializer = UploadImageSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                upload_image(user=user, **serializer.validated_data)
                data = {
                    "Success": True,
                    "msg": "Uploaded Image successfully.",
                }
            return Response(status=status.HTTP_200_OK, data=data)
        except ValidationError as e:
            mes = "\n".join(e.messages)
            raise ValidationError(mes)
        except Exception:
            error_info = "\n".join(traceback.format_exception(*sys.exc_info()))
            print(error_info)
            data = {
                "Success": False,
                "msg": "Uploading failed",
            }
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data)  


class PostListAPI(APIView):
    """API for getting Post list."""

    authentication_classes = [SessionAuthentication]

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            result = Post.objects.all().values("id", "title", "description", "post_type", "created_date", "like", "dislike").order_by("-created_date")
            serializer = PostListSerializer(result, many=True)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        except ValidationError as e:
            mes = "\n".join(e.messages)
            raise ValidationError(mes)
        except Exception:
            error_info = "\n".join(traceback.format_exception(*sys.exc_info()))
            print(error_info)
            data = {
                "Success": False,
                "msg": "List getting failed",
            }
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data)                                 