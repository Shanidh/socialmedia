from django.contrib import admin

# Register your models here.
from adminapp.models import CustomUser

admin.site.register(CustomUser)