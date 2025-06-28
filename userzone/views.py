from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from user_profile.models import UserProfile
from plaza.models import Post as PlazaPost
from moments.models import Post as MomentsPost

def userzone(request, username):
    user_profile = get_object_or_404(UserProfile, user__username=username)
    is_owner = (request.user == user_profile.user)
    plaza_posts = PlazaPost.objects.filter(author=user_profile.user).order_by('-created_at')
    moments_posts = MomentsPost.objects.filter(author=user_profile.user).order_by('-created_at') if is_owner else []
    context = {
        'user_profile': user_profile,
        'is_owner': is_owner,
        'plaza_posts': plaza_posts,
        'moments_posts': moments_posts,
        'recent_visitors': []  # 需实现
    }
    return render(request, 'userzone/userzone.html', context)
