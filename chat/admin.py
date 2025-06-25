from django.contrib import admin
from .models import Message

# Register your models here.
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'timestamp', 'is_read')
    list_filter = ('sender', 'receiver', 'is_read')
    search_fields = ('content',)
