from django.urls import path
from ..apis import userapp


urlpatterns = [
    path("register", userapp.RegisterAPI.as_view(), name="register"),
    path("", userapp.LoginAPI.as_view(), name="login"),
    path("logout", userapp.LogOutAPI.as_view(), name="logout"),
]