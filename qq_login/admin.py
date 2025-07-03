from django.contrib import admin
from .models import QQUser

@admin.register(QQUser)
class QQUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'qq_nickname', 'qq_openid', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'qq_nickname', 'qq_openid']
    readonly_fields = ['created_at', 'updated_at']
