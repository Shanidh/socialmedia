from rest_framework import serializers


class PostListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)    
    title = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    post_type = serializers.CharField(read_only=True)
    created_date = serializers.CharField(read_only=True)
    like = serializers.CharField(read_only=True)
    dislike = serializers.CharField(read_only=True)


class PostImageDetailSerializer(serializers.Serializer):
    Image = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)


class LikedUsersDetailSerializer(serializers.Serializer):
    user__username = serializers.CharField(read_only=True)   


class CurrentUserLikedSerializer(serializers.Serializer):
    status = serializers.CharField(read_only=True)     


class PostLikeSerializer(serializers.Serializer):
    id = serializers.IntegerField()  