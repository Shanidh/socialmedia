from adminapp.models import CustomUser, UserType

def create_user(
    username: str,
    password: str,
) -> None:
    user = CustomUser.objects.create_user(username=username, password=password, user_type=UserType.USER)