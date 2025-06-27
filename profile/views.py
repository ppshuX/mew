from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Profile
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def profile_detail(request, username):
    user = get_object_or_404(User, username=username)
    # 自动创建 profile
    profile, created = Profile.objects.get_or_create(user=user)

    return render(request, 'profile/profile_detail.html', {'profile': user.profile})

@login_required
def profile_edit(request, username):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_detail', username=request.user.username)
        
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile/profile_edit.html', {'form':form})
