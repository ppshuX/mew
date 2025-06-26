from django.shortcuts import render,redirect, get_object_or_404
from .models import Post, Comment
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone

# Create your views here.
@login_required
def moments_list(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')
        if content or image:
            Post.objects.create(author=request.user, content=content, image=image)
            return redirect('moments_list')
        
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
            return redirect(f'/moments/{comment.post.id}/?show_all_comments=1')
        else:
            return redirect(f'/moments/{post_id}/?show_all_comments=1')

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author or request.user.is_superuser:
        comment.delete()
    return redirect('post_detail', post_id=comment.post.id)


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # 判断当前用户是否已点赞
    liked_by_user = request.user in post.likes.all()

    return render(request, 'moments/post_detail.html', {'post': post, 'liked_by_user':liked_by_user})
