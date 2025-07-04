from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.timezone import now

def blog_cover_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4().hex}_{now().strftime('%Y%m%d%H%M%S')}.{ext}"
    return f"blog/covers/{unique_filename}"

# Create your models here.
class BlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    cover_image = models.ImageField(upload_to=blog_cover_upload_to, blank=True, null=True)
    content = models.TextField()
    category = models.CharField(max_length=50, default='未分类')
    is_draft = models.BooleanField(default=False, verbose_name="是否草稿")
    last_saved_time = models.DateTimeField(auto_now=True, verbose_name="最后保存时间")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_blog = models.BooleanField(default=False, verbose_name='是否为博客')
    blog_tags = models.CharField(max_length=200, blank=True, null=True, verbose_name='标签')
    blog_summary = models.CharField(max_length=200, blank=True, null=True, verbose_name='摘要')
    publish_type = models.CharField(max_length=20, default='private', verbose_name='发布到')
    likes = models.ManyToManyField(User, related_name='blog_liked_posts', blank=True)

    def __str__(self):
        return self.title
    
    def like_count(self):
        return self.likes.count()
    
    def comment_count(self):
        """返回评论数，博客暂时返回0"""
        return 0

    def get_summary(self, length=50):
        if not self.content:
            return ''
        return (self.content[:length] + '...') if len(self.content) > length else self.content

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.cover_image:
            try:
                from utils.image_compress import compress_image
                compress_image(self.cover_image.path)
            except Exception:
                pass

def blog_image_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4().hex}_{now().strftime('%Y%m%d%H%M%S')}.{ext}"
    return f"blog_images/{unique_filename}"

class BlogImage(models.Model):
    post = models.ForeignKey(BlogPost, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=blog_image_upload_to)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            from utils.image_compress import compress_image
            compress_image(self.image.path)
        except Exception:
            pass

class BlogComment(models.Model):
    post = models.ForeignKey(BlogPost, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_blog_comments', blank=True)

    def __str__(self):
        return f"{self.author.username}: {self.content[:20]}"

    def like_count(self):
        return self.likes.count()

