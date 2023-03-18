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
    dislike_count = post.dislike
    if LikedPosts.objects.filter(post=post, user=user):
        likepost = LikedPosts.objects.get(post=post, user=user)
        if likepost.status == LikeStatus.LIKE:
            return
        elif likepost.status == LikeStatus.DISLIKE:   
            post.dislike = dislike_count-1
            likepost.status = LikeStatus.LIKE
            post.like = count+1
            likepost.save()
            post.save()
            return
        else:  
            likepost.status = LikeStatus.LIKE
            post.like = count+1
            likepost.save()
            post.save()
            return
    like = LikedPosts(post=post, user=user, status=LikeStatus.LIKE)
    post.like = count+1  
    like.save()
    post.save()  


def post_dislike(
    user: User, 
    id: int
) -> str:
    post = Post.objects.get(pk=id)  
    count = post.dislike
    like_count = post.like
    if LikedPosts.objects.filter(post=post, user=user):
        likepost = LikedPosts.objects.get(post=post, user=user)
        if likepost.status == LikeStatus.DISLIKE:
            return 
        elif likepost.status == LikeStatus.LIKE:   
            post.like = like_count-1
            likepost.status = LikeStatus.DISLIKE
            post.dislike = count+1
            likepost.save()
            post.save()
            return    
        else:  
            likepost.status = LikeStatus.DISLIKE
            post.like = count+1
            likepost.save()
            post.save()
            return
    like = LikedPosts(post=post, user=user, status=LikeStatus.DISLIKE)
    post.dislike = count+1  
    like.save()
    post.save()  