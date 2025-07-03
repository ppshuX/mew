from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.timezone import now

# Create your models here.
class Post(models.Model):
    CATEGORY_CHOICES = [
        ('daily', '日常'),
        ('study', '学习'),
        ('work', '工作'),
        ('travel', '旅行'),
        ('food', '美食'),
        ('sports', '运动'),
        ('entertainment', '娱乐'),
        ('other', '其他'),
    ]
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='moments_posts')
    content = models.TextField(max_length=5000)
    # image = models.ImageField(upload_to='moments_posts/', blank=True, null=True)  # 已弃用，改为多图
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='daily', verbose_name='类别')
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    is_private = models.BooleanField(default=False, verbose_name='私密动态')

    def like_count(self):
        return self.likes.count()
    
    def comment_count(self):
        return self.comments.count()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='moments_comments')
    content = models.TextField(max_length=3000)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='moments_liked_comments', blank=True)

    def like_count(self):
        return self.likes.count()
    
    def is_liked_by(self, user):
        return self.likes.filter(id=user.id).exists()

def moments_image_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4().hex}_{now().strftime('%Y%m%d%H%M%S')}.{ext}"
    return f"moments_images/{unique_filename}"

class MomentsImage(models.Model):
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=moments_image_upload_to)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"图片 - {self.post.author.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
