from django.contrib.auth import get_user_model
from rest_framework.response import Response

from adminapp.models import Post
from ..models import LikedPosts, LikeStatus


User = get_user_model()


def post_like(
    user: User, 
    id: int
) -> str:
    post = Post.objects.get(pk=id)  
    count = post.like
    if LikedPosts.objects.filter(post=post, user=user):
        likepost = LikedPosts.objects.get(post=post, user=user)
        if likepost.status == LikeStatus.LIKE:
            data = {'message': 'Already liked!'}
            return Response(data)
        else:  
            likepost.status = LikeStatus.LIKE
            post.like = count+1
            likepost.save()
            post.save()
            data = {'message': 'Like updated!'}
            return Response(data)
    like = LikedPosts(post=post, user=user, status=LikeStatus.LIKE)
    post.like = count+1  
    like.save()
    post.save()  

