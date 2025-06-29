import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mew.settings')
django.setup()

from moments.models import Post as MomentsPost
from plaza.models import Post as PlazaPost

# moments
moments_fixed = 0
for post in MomentsPost.objects.all():
    if not post.category:
        post.category = 'daily'
        post.save()
        moments_fixed += 1

# plaza
plaza_fixed = 0
for post in PlazaPost.objects.all():
    if not post.category:
        post.category = 'daily'
        post.save()
        plaza_fixed += 1

print(f"已修复 moments 动态 {moments_fixed} 条，plaza 动态 {plaza_fixed} 条，全部补为 daily 类别。") 