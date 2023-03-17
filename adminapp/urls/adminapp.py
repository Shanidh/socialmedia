from django.urls import path
from ..apis import adminapp


urlpatterns = [
    path("register", adminapp.RegisterAPI.as_view(), name="register"),
]