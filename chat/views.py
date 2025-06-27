from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Message
from django.contrib.auth.models import User
from profile.models import Profile

# Create your views here.
@login_required
def chat_view(request):
    users = User.objects.exclude(id=request.user.id).select_related('profile')
    selected_user = None
    messages = []

    if request.method == 'GET':
        receiver_id = request.GET.get('user')
        if receiver_id:
            selected_user = User.objects.get(id=receiver_id)
            messages = Message.objects.filter(
                sender__in=[request.user, selected_user],
                receiver__in=[request.user, selected_user]
            ).order_by('timestamp')
    
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver_id')
        content = request.POST.get('content')
        if receiver_id and content:
            receiver = User.objects.get(id=receiver_id)
            Message.objects.create(sender=request.user, receiver=receiver, content=content)
            return redirect(f'/chat/?user={receiver.id}')
    
    return render(request, 'chat/chat.html', {
        'users': users,
        'selected_user': selected_user,
        'messages': messages,
    })
