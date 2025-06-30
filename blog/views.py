from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost, BlogImage
from .forms import BlogPostForm
from moments.models import Post as MomentsPost, MomentsImage
from plaza.models import Post as PlazaPost, PostImage as PlazaPostImage
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.
@login_required
def blog_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            for img in request.FILES.getlist('images'):
                BlogImage.objects.create(post=post, image=img)
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
                # 同步多图到朋友圈
                for img in post.images.all():
                    MomentsImage.objects.create(post=moments_post, image=img.image)
                return redirect('moments:post_detail', post_id=moments_post.pk)
            elif publish_type == 'plaza':
                plaza_post = PlazaPost.objects.create(
                    author=request.user,
                    content=content,
                    image=image,
                    category=category
                )
                # 同步多图到广场
                for img in post.images.all():
                    PlazaPostImage.objects.create(post=plaza_post, image=img.image)
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
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog_detail', pk=pk)
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blog/blog_form.html', {'form':form, 'post': post})

@login_required
def create_post(request):
    if request.method == 'POST':
        is_blog = 'blog_title' in request.POST
        if is_blog:
            post = BlogPost(
                author=request.user,
                title=request.POST.get('blog_title'),
                content=request.POST.get('blog_content'),
                cover_image=request.FILES.get('blog_cover'),
                category=request.POST.get('category'),
                is_blog=True,
                blog_tags=request.POST.get('blog_tags'),
                blog_summary=request.POST.get('blog_summary'),
                is_draft='draft' in request.POST,
                publish_type=request.POST.get('publish_type', 'private'),
            )
        else:
            post = BlogPost(
                author=request.user,
                title=request.POST.get('title'),
                content=request.POST.get('content'),
                cover_image=request.FILES.get('cover_image'),
                category=request.POST.get('category'),
                is_blog=False,
                is_draft='draft' in request.POST,
                publish_type=request.POST.get('publish_type', 'private'),
            )
        post.save()
        return redirect('userzone:detail', request.user.username)
    else:
        form = BlogPostForm()
    return render(request, 'blog/blog_form.html', {'form': form})

@login_required
def draft_list(request):
    drafts = BlogPost.objects.filter(author=request.user, is_draft=True).order_by('-updated_at')
    paginator = Paginator(drafts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/draft_list.html', {'page_obj': page_obj})

CATEGORY_CHOICES = [
    ('daily', '日常'),
    ('study', '学习'),
    ('work', '工作'),
    ('travel', '旅行'),
    ('food', '美食'),
    ('sports', '运动'),
    ('entertainment', '娱乐'),
    ('other', '其他'),
]

@login_required
def simple_create(request):
    if request.method == 'POST':
        post = BlogPost(
            author=request.user,
            title=request.POST.get('title'),
            content=request.POST.get('content'),
            category=request.POST.get('category'),
            is_blog=False,
            publish_type=request.POST.get('publish_type', 'private'),
        )
        post.save()
        # 图片上传等可后续扩展
        return redirect('userzone:detail', request.user.username)
    return render(request, 'blog/blog_form_simple.html', {'category_choices': CATEGORY_CHOICES})