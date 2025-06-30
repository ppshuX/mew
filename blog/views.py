from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost
from .forms import BlogPostForm
from moments.models import Post as MomentsPost
from plaza.models import Post as PlazaPost
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def blog_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            content = form.cleaned_data['content']
            title = form.cleaned_data.get('title', '').strip()
            if title:
                content = f"【{title}】\n\n{content}"
            publish_type = form.cleaned_data.get('publish_type', 'private')
            image = form.cleaned_data.get('cover_image')
            category = form.cleaned_data.get('category', 'daily')
            if publish_type == 'moments':
                moments_post = MomentsPost.objects.create(
                    author=request.user,
                    content=content,
                    image=image,
                    category=category,
                    is_private=False
                )
                return redirect('moments:post_detail', post_id=moments_post.pk)
            elif publish_type == 'plaza':
                plaza_post = PlazaPost.objects.create(
                    author=request.user,
                    content=content,
                    image=image,
                    category=category
                )
                return redirect('plaza:detail', post_id=plaza_post.pk)
            else:
                moments_post = MomentsPost.objects.create(
                    author=request.user,
                    content=content,
                    image=image,
                    category=category,
                    is_private=True
                )
                return redirect('moments:post_detail', post_id=moments_post.pk)
    else:
        form = BlogPostForm()
    return render(request, 'blog/blog_form.html', {'form': form})

def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if post.is_draft and post.author != request.user:
        return redirect('home')
    return render(request, 'blog/blog_detail.html', {'post':post})

@login_required
def blog_edit(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if post.author != request.user:
        return redirect('blog_detail', pk=pk)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog_detail', pk=pk)
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blog/blog_form.html', {'form':form, 'post': post})