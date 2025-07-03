import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mew.settings')
django.setup()

from django.contrib.auth.models import User
from user_profile.models import UserProfile
from blog.models import BlogImage, BlogPost
from moments.models import Post as MomentsPost, MomentsImage, Comment as MomentsComment
from plaza.models import Post, PostImage, Comment as PlazaComment

# 删除所有评论
PlazaComment.objects.all().delete()
MomentsComment.objects.all().delete()

# 删除所有动态/帖子
PostImage.objects.all().delete()
Post.objects.all().delete()
MomentsImage.objects.all().delete()
MomentsPost.objects.all().delete()

# 删除所有博客图片和博客
BlogImage.objects.all().delete()
BlogPost.objects.all().delete()

# 删除所有用户资料
UserProfile.objects.all().delete()

# 删除所有用户
User.objects.all().delete()

print("所有用户及相关数据已清空！") 