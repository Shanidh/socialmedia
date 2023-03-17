from adminapp.models import CustomUser, UserType
from django.contrib.auth import get_user_model

from ..models import Post, Tag

User = get_user_model()

def create_admin_user(
    username: str,
    password: str,
) -> None:
    user = CustomUser.objects.create_user(username=username, password=password, user_type=UserType.ADMIN)


def create_post(
    user: User,
    title: str,
    post_type: str,
    description: str,
) -> None:
    post = Post(
        title=title,
        description=description,
        post_type=post_type,
    )
    post.save()
    if Tag.objects.filter(name=post_type).exists():
        tag = Tag.objects.get(name=post_type)
        count = tag.weight
        if tag.name == post_type:
            tag.weight=count+1
            tag.save()
    else:
        tags = Tag(name=post_type, weight=1) 
        tags.save()      