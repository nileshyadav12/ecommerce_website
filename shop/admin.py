from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from shop.models import CustomUser

# This line is already registering CustomUser with UserAdmin, so you don't need it again below.
admin.site.register(CustomUser, UserAdmin)
