from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import UserProfileForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def user_profile_detail(request, username):
    user = get_object_or_404(User, username=username)
    user_profile = get_object_or_404(UserProfile, user=user)
    return render(request, 'user_profile/user_profile_detail.html', {'user_profile': user_profile})

@login_required
def user_profile_edit(request, username):
    user_profile = request.user.user_profile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile_detail', username=request.user.username)
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'user_profile/user_profile_edit.html', {'form':form})
