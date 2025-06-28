from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Like, Comment
from django.contrib.auth.decorators import login_required

def plaza_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'plaza/plaza.html', {'posts': posts})

def plaza_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'plaza/detail.html', {'post': post})

@login_required
def plaza_add_comment(request, post_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(post_id=post_id, author=request.user, content=content)
    return redirect('plaza:detail', post_id=post_id)

@login_required
def plaza_like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    Like.objects.get_or_create(post=post, user=request.user)
    return redirect('plaza:list')

@login_required
def plaza_delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author == request.user:
        comment.delete()
    return redirect('plaza:detail', post_id=comment.post.id)

@login_required
def plaza_like_comment(request, comment_id):
    # 你可以设计一个 CommentLike 模型来支持这一功能
    return redirect('plaza:detail', post_id=comment_id)  # 这里先占位
