from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plaza_posts')
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=3000)
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

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
