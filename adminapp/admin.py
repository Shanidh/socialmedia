from django.contrib import admin

# Register your models here.
from adminapp.models import CustomUser, Post, Tag

admin.site.register(CustomUser)
admin.site.register(Post)
admin.site.register(Tag)