from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from shop.models import CustomUser

# This line is already registering CustomUser with UserAdmin, so you don't need it again below.
admin.site.register(CustomUser, UserAdmin)
# admin.py
from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
