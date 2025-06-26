from django.shortcuts import render,redirect, get_object_or_404
from .models import Post, Comment, Like
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
            return redirect('moments')
        
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'moments/moments.html',{'posts': posts})


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    return JsonResponse({'liked': liked, 'like_count': post.like_count()})


@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        content = request.POST.get('comment')
        post = get_object_or_404(Post, id=post_id)
        if content:
            Comment.objects.create(post=post, author=request.user, content=content)
    return redirect('moments')

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author or request.user.is_superuser:
        comment.delete()
    return redirect('moments_list')
