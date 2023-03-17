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
from adminapp.models import CustomUser
from django.shortcuts import render, redirect

from ..serializers import (
    CreateAdminUserSerializer,
)

from ..services import (
    create_admin_user,
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