from rest_framework import serializers


class CreateAdminUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class CreatePostSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()   
    post_type = serializers.CharField() 