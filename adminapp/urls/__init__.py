from django.urls import re_path as url
from django.conf.urls import include
from django.urls import path

app_name = "adminapp"

urlpatterns = [
    url("admin/", include("adminapp.urls.adminapp")),
]