from adminapp.models import CustomUser, UserType
from django.contrib.auth import get_user_model
from django.core.files.storage import FileSystemStorage

from ..models import Post, Tag, Image

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


def upload_image(
    user: User,
    image: str,
    description: str,
    post_id=int,
) -> None:  
    post = Post.objects.get(pk=post_id)  
    ext = os.path.splitext(image)[1]
    valid_extensions = [".jpg", ".jpeg", ".png"]
    if not ext in valid_extensions:
        data = {
                "Success": False,
                "msg": "File not supported!",
            }
        return Response(status=status.HTTP_400_BAD_REQUEST, data=data)
        # raise ValidationError(_("File not supported!"))  
    obj1 = FileSystemStorage()
    obj1.save(image)  
    imageupload = Image(image=image, description=description, post=post) 
    imageupload.save()   
    return imageupload

