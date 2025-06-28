from django.shortcuts import render,redirect, get_object_or_404
from .models import Post, Comment
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import CustomRegisterForm
from django.contrib import messages

# Create your views here.
@login_required
def  moments_list(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')
        if content or image:
            Post.objects.create(author=request.user, content=content, image=image)
            return redirect('moments:list')
        
    posts = Post.objects.all().order_by('-created_at')
    # ⭐ 添加判断：当前用户是否点赞了每个 post
    for post in posts:
        post.is_liked = request.user in post.likes.all()

    return render(request, 'moments/moments.html',{'posts': posts})

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
            return redirect('post_detail', post_id=comment.post.id)
        else:
            return redirect('post_detail', post_id=post_id)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author or request.user.is_superuser:
        comment.delete()
    return redirect('post_detail', post_id=comment.post.id)


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
            form.save()
            return redirect('login')
    else:
        form = CustomRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


#评论点赞视图
@require_POST
@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    user = request.user
    
    print(f"评论点赞请求: 评论ID={comment_id}, 用户={user.username}")
    print(f"当前点赞状态: {user in comment.likes.all()}")

    if user in comment.likes.all():
        comment.likes.remove(user)
        liked = False
        print(f"取消点赞: 用户={user.username}, 评论ID={comment_id}")
    else:
        comment.likes.add(user)
        liked = True
        print(f"添加点赞: 用户={user.username}, 评论ID={comment_id}")

    # 确保数据保存到数据库
    comment.save()
    
    like_count = comment.like_count()
    print(f"点赞后状态: liked={liked}, like_count={like_count}")

    return JsonResponse({
        'liked': liked,
        'like_count': like_count
    })

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author or request.user.is_superuser:
        post.delete()
        messages.success(request, '动态已删除')
        return redirect('moments:list')
    else:
        messages.error(request, '你没有权限删除该动态')
        return redirect('moments:post_detail', post_id=post_id)