from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# 上传头像的路径函数
def user_directory_path(instance, filename):
    return f'avatars/user_{instance.user.id}/{filename}'

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField(verbose_name="消息内容")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="发送时间")
    is_read = models.BooleanField(default=False, verbose_name="是否已读")

    def __str__(self):
        return f'{self.sender.username} → {self.receiver.username}: {self.content[:20]}'
