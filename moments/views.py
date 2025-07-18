from django.shortcuts import render,redirect, get_object_or_404
from .models import Post, Comment, MomentsImage
from blog.models import BlogPost
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import CustomRegisterForm
from django.contrib import messages
from itertools import chain
from operator import attrgetter
from django.urls import reverse
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import io
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from .forms import LoginForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode

# Create your views here.
@login_required
def  moments_list(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        images = request.FILES.getlist('images')
        category = request.POST.get('category', 'daily')
        is_private = request.POST.get('is_private') == 'true'  # 处理私密发送
        if content or images:
            post = Post.objects.create(author=request.user, content=content, category=category, is_private=is_private)
            for img in images[:9]:
                try:
                    MomentsImage.objects.create(post=post, image=img)
                except Exception as e:
                    pass
            return redirect('moments:list')
        
    # 获取普通动态
    posts = Post.objects.filter(is_private=False).order_by('-created_at')
    # 获取博客动态（发布到朋友圈的博客）
    blog_posts = BlogPost.objects.filter(
        is_draft=False,
        is_blog=True,
        publish_type__icontains='moments'
    ).order_by('-created_at')
    
    # 合并两种类型的内容并按时间排序
    all_content = list(chain(posts, blog_posts))
    all_content.sort(key=attrgetter('created_at'), reverse=True)
    
    # ⭐ 添加判断：当前用户是否点赞了每个 post
    for item in all_content:
        if isinstance(item, BlogPost):
            item.is_liked = False
            item.content_type = 'blog'
        else:
            item.is_liked = request.user in item.likes.all()
            item.content_type = 'post'

    return render(request, 'moments/moments.html',{'posts': all_content})

@require_POST
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True

    return JsonResponse({'liked': liked, 'like_count': post.like_count()})


@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        content = request.POST.get('comment')
        post = get_object_or_404(Post, id=post_id)
        if content:
            comment = Comment.objects.create(post=post, author=request.user, content=content)
            return redirect('moments:post_detail', post_id=comment.post.id)
        else:
            return redirect('moments:post_detail', post_id=post_id)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author or request.user.is_superuser:
        comment.delete()
    return redirect('moments:post_detail', post_id=comment.post.id)


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    liked_by_user = request.user in post.likes.all()
    comments = []
    for comment in post.comments.all():
        comments.append({
            'obj': comment,
            'liked_by_user': request.user in comment.likes.all(),
        })
    return render(request, 'moments/post_detail.html', {
        'post': post,
        'liked_by_user': liked_by_user,
        'comments': comments,
    })


def register(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.is_active = False
            user.save()
            # 发送激活邮件
            current_site = get_current_site(request)
            subject = 'Mew账号激活邮件'
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            activation_link = f"http://{current_site.domain}/accounts/activate/{uid}/{token}/"
            message = render_to_string('accounts/activation_email.html', {
                'user': user,
                'activation_link': activation_link,
            })
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
            # messages.success(request, '注册成功！请前往邮箱激活账号。')
            return render(request, 'accounts/register_success.html')
    else:
        form = CustomRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


#评论点赞视图
@require_POST
@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    user = request.user
    
    if user in comment.likes.all():
        comment.likes.remove(user)
        liked = False
    else:
        comment.likes.add(user)
        liked = True

    # 确保数据保存到数据库
    comment.save()
    
    like_count = comment.like_count()

    return JsonResponse({
        'liked': liked,
        'like_count': like_count
    })

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        messages.error(request, '你没有权限删除该动态。')
        return redirect('moments:post_detail', post_id=post_id)
    if request.method == 'POST':
        post.delete()
        messages.success(request, '动态已删除。')
        return redirect('moments:list')
    else:
        return render(request, 'moments/moments_confirm_delete.html', {'post': post})

def compress_image(uploaded_file, quality=70, max_size=1024):
    image = Image.open(uploaded_file)
    if max(image.size) > max_size:
        ratio = max_size / max(image.size)
        new_size = (int(image.size[0]*ratio), int(image.size[1]*ratio))
        image = image.resize(new_size, Image.Resampling.LANCZOS)
    output_io = io.BytesIO()
    image = image.convert('RGB')
    image.save(output_io, format='JPEG', quality=quality)
    output_io.seek(0)
    return InMemoryUploadedFile(
        output_io, 'ImageField', uploaded_file.name, 'image/jpeg', output_io.getbuffer().nbytes, None
    )

def test_upload(request):
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        print("收到图片数量：", len(images))
        from .models import Post, MomentsImage
        # 这里随便找一条 Post 关联图片（仅测试用）
        post = Post.objects.first()
        for img in images:
            MomentsImage.objects.create(post=post, image=img)
        return render(request, 'moments/test_upload.html', {'msg': '上传完成'})
    return render(request, 'moments/test_upload.html')

def login_view(request):
    # 获取失败次数
    fail_count = request.session.get('login_fail_count', 0)
    show_captcha = fail_count >= 2
    if request.method == 'POST':
        form = LoginForm(request.POST, show_captcha=show_captcha)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['login_fail_count'] = 0  # 登录成功清零
                return redirect('moments:list')
            else:
                request.session['login_fail_count'] = fail_count + 1
                form.add_error(None, '用户名或密码错误')
        else:
            request.session['login_fail_count'] = fail_count + 1
    else:
        form = LoginForm(show_captcha=show_captcha)
    return render(request, 'accounts/login.html', {'form': form, 'show_captcha': show_captcha})

def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, '账号激活成功，请登录！')
        return redirect('login')
    else:
        messages.error(request, '激活链接无效或已过期。')
        return redirect('register')
