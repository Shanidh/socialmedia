from django.urls import path
from ..apis import adminapp


urlpatterns = [
    path("register", adminapp.RegisterAPI.as_view(), name="register"),
    path("login", adminapp.LoginAPI.as_view(), name="login"),
    path("logout", adminapp.LogOutAPI.as_view(), name="logout"),
]