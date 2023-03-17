from django.urls import path
from ..apis import adminapp
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("register", adminapp.RegisterAPI.as_view(), name="register"),
    path("login", adminapp.LoginAPI.as_view(), name="login"),
    path("logout", adminapp.LogOutAPI.as_view(), name="logout"),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)