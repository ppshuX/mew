from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    cover_image = models.ImageField(upload_to='blog/covers/', blank=True, null=True)
    content = models.TextField()
    category = models.CharField(max_length=50, default='未分类')
    is_draft = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_blog = models.BooleanField(default=False, verbose_name='是否为博客')
    blog_tags = models.CharField(max_length=200, blank=True, null=True, verbose_name='标签')
    blog_summary = models.CharField(max_length=200, blank=True, null=True, verbose_name='摘要')
    publish_type = models.CharField(max_length=20, default='private', verbose_name='发布到')

    def __str__(self):
        return self.title

class BlogImage(models.Model):
    post = models.ForeignKey(BlogPost, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog_images/')
