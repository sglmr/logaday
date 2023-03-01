from django.contrib import admin
from .models import User
from authtools.admin import NamedUserAdmin


admin.site.register(User, NamedUserAdmin)
