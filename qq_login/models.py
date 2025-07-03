from django.db import models
from django.contrib.auth.models import User

class QQUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='qq_user')
    qq_openid = models.CharField(max_length=100, unique=True, verbose_name='QQ OpenID')
    qq_nickname = models.CharField(max_length=100, blank=True, verbose_name='QQ昵称')
    qq_avatar = models.URLField(blank=True, verbose_name='QQ头像')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = 'QQ用户'
        verbose_name_plural = 'QQ用户'

    def __str__(self):
        return f"{self.user.username} ({self.qq_nickname})"
