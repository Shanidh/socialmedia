from django.contrib import admin

# Register your models here.
from adminapp.models import CustomUser, Post

admin.site.register(CustomUser)
admin.site.register(Post)