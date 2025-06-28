from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='moments_posts')
    content = models.TextField(max_length=500)
    image = models.ImageField(upload_to='moments_posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

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
