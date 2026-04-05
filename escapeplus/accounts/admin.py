from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'nickname', 'email', 'kakao_id', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('추가 정보', {'fields': ('kakao_id', 'nickname', 'profile_image')}),
    )
