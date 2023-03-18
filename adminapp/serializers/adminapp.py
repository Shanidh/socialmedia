from rest_framework import serializers


class CreateAdminUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class CreatePostSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()   
    post_type = serializers.CharField() 


class UploadImageSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()  
    image = serializers.CharField()
    description = serializers.CharField()


class PostListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)    
    title = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    post_type = serializers.CharField(read_only=True)
    created_date = serializers.CharField(read_only=True)
    like = serializers.CharField(read_only=True)
    dislike = serializers.CharField(read_only=True)