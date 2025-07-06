from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Message
from django.contrib.auth.models import User
from user_profile.models import UserProfile

# 判断是否为移动端
MOBILE_UA_KEYWORDS = ['Mobile', 'Android', 'iPhone', 'iPad', 'iPod', 'Windows Phone', 'MQQBrowser']
def is_mobile(request):
    ua = request.META.get('HTTP_USER_AGENT', '')
    return any(keyword in ua for keyword in MOBILE_UA_KEYWORDS)

# Create your views here.
@login_required
def chat_view(request, username=None):
    users = User.objects.exclude(id=request.user.id).select_related('user_profile')
    selected_user = None
    messages = []

    if request.method == 'GET':
        receiver_id = request.GET.get('user')
        # 优先使用路由参数 username
        username_param = username or request.GET.get('username')
        if receiver_id:
            selected_user = User.objects.get(id=receiver_id)
            messages = Message.objects.filter(
                sender__in=[request.user, selected_user],
                receiver__in=[request.user, selected_user]
            ).select_related('sender__user_profile').order_by('timestamp')
        elif username_param:
            try:
                selected_user = User.objects.get(username=username_param)
                messages = Message.objects.filter(
                    sender__in=[request.user, selected_user],
                    receiver__in=[request.user, selected_user]
                ).select_related('sender__user_profile').order_by('timestamp')
            except User.DoesNotExist:
                selected_user = None
                messages = []

    if request.method == 'POST':
        receiver_id = request.POST.get('receiver_id')
        content = request.POST.get('content')
        if receiver_id and content:
            receiver = User.objects.get(id=receiver_id)
            Message.objects.create(sender=request.user, receiver=receiver, content=content)
            # 判断来源页面，移动端跳转到/chat/username/，PC端跳转到?user=ID
            if is_mobile(request):
                return redirect(f'/chat/{receiver.username}/')
            else:
                return redirect(f'/chat/?user={receiver.id}')

    # 判断是否为移动端，渲染不同模板
    if is_mobile(request) and selected_user:
        return render(request, 'chat/chat_mobile.html', {
            'users': users,
            'selected_user': selected_user,
            'messages': messages,
        })
    else:
        return render(request, 'chat/chat.html', {
            'users': users,
            'selected_user': selected_user,
            'messages': messages,
        })
