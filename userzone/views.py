from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from user_profile.models import UserProfile
from plaza.models import Post as PlazaPost
from moments.models import Post as MomentsPost
from moments.forms import MomentsPostForm
from userzone.models import UserZoneVisitor
from django.utils import timezone

def userzone(request, username):
    try:
        user_profile = get_object_or_404(UserProfile, user__username=username)
    except:
        # 如果用户没有UserProfile，创建一个
        user = get_object_or_404(User, username=username)
        user_profile = UserProfile.objects.create(user=user)
    
    is_owner = (request.user == user_profile.user)
    
    # 记录访客（仅非本人且已登录用户）
    if request.user.is_authenticated and not is_owner:
        try:
            visitor_profile = request.user.user_profile
            obj, created = UserZoneVisitor.objects.get_or_create(userzone_owner=user_profile, visitor=visitor_profile)
            obj.visited_at = timezone.now()
            obj.save()
        except Exception as e:
            print('记录访客失败:', e)

    # 获取最近访客（最新30个）
    recent_visitor_objs = UserZoneVisitor.objects.filter(userzone_owner=user_profile).select_related('visitor').order_by('-visited_at')[:30]
    recent_visitors = [v.visitor for v in recent_visitor_objs]
    
    # 获取筛选参数
    post_type = request.GET.get('type', 'moments').strip()  # moments, plaza, private
    category = request.GET.get('category', 'all').strip()   # all, daily, study, work, etc.
    
    if is_owner:
        moments_posts = MomentsPost.objects.filter(author=user_profile.user, is_private=False).order_by('-created_at')
        private_posts = MomentsPost.objects.filter(author=user_profile.user, is_private=True).order_by('-created_at')
    else:
        moments_posts = MomentsPost.objects.filter(author=user_profile.user, is_private=False).order_by('-created_at')
        private_posts = []
    
    plaza_posts = PlazaPost.objects.filter(author=user_profile.user).order_by('-created_at')
    
    # 按类别筛选
    if category != 'all':
        moments_posts = moments_posts.filter(category=category)
        plaza_posts = plaza_posts.filter(category=category)
        private_posts = private_posts.filter(category=category)
    
    form = None
    if is_owner:
        if request.method == 'POST':
            form = MomentsPostForm(request.POST, request.FILES)
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.author = request.user
                new_post.save()
                form.save_m2m()
                return redirect('userzone', username=username)
        else:
            form = MomentsPostForm()
    
    # 获取所有类别选项
    category_choices = MomentsPost.CATEGORY_CHOICES
    
    context = {
        'user_profile': user_profile,
        'is_owner': is_owner,
        'plaza_posts': plaza_posts,
        'moments_posts': moments_posts,
        'private_posts': private_posts,
        'recent_visitors': recent_visitors,
        'form': form,
        'current_type': post_type,
        'current_category': category,
        'category_choices': category_choices,
    }
    return render(request, 'userzone/userzone.html', context)
