from django.db import models
from django.contrib.auth.models import User

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
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plaza_posts')
    content = models.TextField(max_length=500)
    image = models.ImageField(upload_to='plaza_posts/', blank=True, null=True)  # 保留单图片字段以兼容旧数据
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='daily', verbose_name='类别')
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='plaza_liked_posts', blank=True)

    def like_count(self):
        return self.likes.count()
    
    def comment_count(self):
        return self.plaza_comments.count()

    def __str__(self):
        return f"{self.author.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class PostImage(models.Model):
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='plaza_posts/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"图片 - {self.post.author.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='plaza_comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plaza_comments')
    content = models.TextField(max_length=3000)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='plaza_liked_comments', blank=True)

    def like_count(self):
        return self.likes.count()
    
    def is_liked_by(self, user):
        return self.likes.filter(id=user.id).exists()

class Meta:
    unique_together = ('post', 'user')
