from django.urls import path
from ..apis import userpost


urlpatterns = [
    path("post/list", userpost.PostListAPI.as_view(), name="post_list"),
    path("post/list/<int:id>", userpost.PostDetailAPI.as_view(), name="post_detail"),
    path("post/like", userpost.PostLikeAPI.as_view(), name="post_like"),
    path("post/dislike", userpost.PostDislikeAPI.as_view(), name="post_dislike"),
]