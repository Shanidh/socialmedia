from rest_framework import serializers


class CreateAdminUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()