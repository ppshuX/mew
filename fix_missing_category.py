import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mew.settings')
django.setup()

from moments.models import Post as MomentsPost
from plaza.models import Post as PlazaPost
from django.contrib.auth.models import User

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

def create_test_post():
    user = User.objects.first()
    if not user:
        print('没有用户，请先创建用户')
        return
    post = PlazaPost.objects.create(author=user, content='测试内容')
    print(f'已创建Post，id={post.id}')

def create_moments_test_post():
    user = User.objects.first()
    if not user:
        print('没有用户，请先创建用户')
        return
    post = MomentsPost.objects.create(author=user, content='朋友圈测试内容')
    print(f'已创建Moments Post，id={post.id}')

if __name__ == '__main__':
    create_test_post()
    create_moments_test_post() 