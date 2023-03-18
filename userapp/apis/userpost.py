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
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import transaction
from django.shortcuts import render, redirect
from rest_framework.permissions import IsAuthenticated
from adminapp.models import Post, Image
from ..models import LikedPosts, LikeStatus

from ..seriliazers import (
    PostListSerializer,
    PostImageDetailSerializer,
    LikedUsersDetailSerializer,
    CurrentUserLikedSerializer,
    PostLikeSerializer,
)

from ..services import (
    post_like,
    post_dislike,
)


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


class PostDetailAPI(APIView):
    """API for getting Post Detail."""

    authentication_classes = [SessionAuthentication]

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        user = request.user
        try:
            post = Post.objects.get(pk=id)
            post_serializer = PostListSerializer(post)
            if Image.objects.filter(post_id=id).exists() and LikedPosts.objects.filter(post_id=id).exists():
                image = Image.objects.filter(post_id=id)
                image_serializer = PostImageDetailSerializer(image)
                likedusers = LikedPosts.objects.filter(post_id=id, status=LikeStatus.LIKE)
                likedusers_serializer = LikedUsersDetailSerializer(likedusers)
                if LikedPosts.objects.filter(post_id=id, user=user).exists():                
                    userliked = LikedPosts.objects.get(post_id=id, user=user)
                    userliked_serializer = CurrentUserLikedSerializer(userliked)
                    dict = {
                        "post_detail": post_serializer.data,
                        "image_detail": image_serializer.data,
                        "likedusers": likedusers_serializer.data,
                        "like": userliked_serializer.data,
                    }
                else:
                    dict = {
                        "post_detail": post_serializer.data,
                        "image_detail": image_serializer.data,
                        "likedusers": likedusers_serializer.data,
                        "like": "None",
                    }    
            elif Image.objects.filter(post_id=id).exists():
                image = Image.objects.filter(post_id=id)
                image_serializer = PostImageDetailSerializer(image)  
                dict = {
                    "image_detail": image_serializer.data,
                    "post_detail": post_serializer.data,
                    "likedusers": "None",
                    "like": "None",
                }
            elif LikedPosts.objects.filter(post_id=id).exists():
                likedusers = LikedPosts.objects.filter(post_id=id, status=LikeStatus.LIKE)
                likedusers_serializer = LikedUsersDetailSerializer(likedusers)
                if LikedPosts.objects.filter(post_id=id, user=user).exists():                
                    userliked = LikedPosts.objects.get(post_id=id, user=user)
                    userliked_serializer = CurrentUserLikedSerializer(userliked)
                    dict = {
                        "post_detail": post_serializer.data,
                        "image_detail": "None",
                        "likedusers": likedusers_serializer.data,
                        "like": userliked_serializer.data,
                    }
                else:
                    dict = {
                        "post_detail": post_serializer.data,
                        "image_detail": "None",
                        "likedusers": likedusers_serializer.data,
                        "like": "None",
                    }   
            else:
                dict = {
                    "post_detail": post_serializer.data,
                    "image_detail": "None",
                    "likedusers": "None",
                    "like": "None",
                    }    
            return Response(status=status.HTTP_200_OK, data=dict)
        except ValidationError as e:
            mes = "\n".join(e.messages)
            raise ValidationError(mes)
        except Exception:
            error_info = "\n".join(traceback.format_exception(*sys.exc_info()))
            print(error_info)
            data = {
                "Success": False,
                "msg": "Detail getting failed",
            }
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data)        


class PostLikeAPI(APIView):
    authentication_classes = [SessionAuthentication]

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        try:
            serializer = PostLikeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                result = post_like(user=user, **serializer.validated_data)
                data = {
                    "Success": True,
                    "msg": "Liked successfully.",
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
                "msg": "Post liking failed",
            }
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data)


class PostDislikeAPI(APIView):
    authentication_classes = [SessionAuthentication]

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        try:
            serializer = PostLikeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                result = post_dislike(user=user, **serializer.validated_data)
                data = {
                    "Success": True,
                    "msg": "Disliked successfully.",
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
                "msg": "Post disliking failed",
            }
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data)                               