from django.db import models
from django.contrib.auth.models import User

# Create your models here.

def user_directory_path(instance, filename):
    return f'avatars/user_{instance.user.id}/{filename}'

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('F', '女'),
        ('M', '男'),
        ('S', '保密'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    avatar = models.ImageField(upload_to=user_directory_path, default='avatars/default.jpg', verbose_name='头像')
    nickname = models.CharField(max_length=30, blank=True, verbose_name='昵称')
    bio = models.TextField(max_length=500, blank=True, verbose_name='签名')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, verbose_name='性别')
    birthday = models.DateField(null=True, blank=True, verbose_name='生日')
    location = models.CharField(max_length=50, blank=True, verbose_name='所在地')
    school = models.CharField(max_length=100, blank=True, verbose_name='学校')
    ip_location = models.CharField(max_length=100, blank=True, verbose_name='IP位置')
    is_online = models.BooleanField(default=False, verbose_name='在线状态')
    following_count = models.IntegerField(default=0, verbose_name='关注数')
    follower_count = models.IntegerField(default=0, verbose_name='粉丝数')
    view_count = models.IntegerField(default=0, verbose_name='阅读量')

    def __str__(self):
        return f"{self.user.username}的资料"
