from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost, BlogImage
from .forms import BlogPostForm
from moments.models import Post as MomentsPost, MomentsImage
from plaza.models import Post as PlazaPost, PostImage as PlazaPostImage
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import os, uuid
from django.conf import settings
from django.contrib import messages
import markdown
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import io

# Create your views here.
@login_required
def blog_create(request):
    if request.method == 'POST':
        is_draft = str(request.POST.get('is_draft', '')).lower() in ['true', '1']
        publish_to = request.POST.getlist('publish_to')
        publish_type = ','.join(sorted(set([x for x in publish_to if x in ['blog', 'moments', 'plaza', 'private']])))
        cover = request.FILES.get('blog_cover')
        cover_image = compress_image(cover) if cover else None
        post = BlogPost(
            author=request.user,
            title=request.POST.get('blog_title'),
            content=request.POST.get('blog_content'),
            cover_image=cover_image,
            category=request.POST.get('category', 'daily'),
            is_blog=True,
            blog_tags=request.POST.get('blog_tags'),
            blog_summary=request.POST.get('blog_summary'),
            is_draft=is_draft,
            publish_type=publish_type or 'blog',
        )
        post.save()
        for img in request.FILES.getlist('images'):
            try:
                compressed_img = compress_image(img)
                BlogImage.objects.create(post=post, image=compressed_img)
            except Exception as e:
                print("图片保存失败：", e)
                import traceback; traceback.print_exc()
        return redirect('blog_detail', pk=post.id)
    else:
        form = BlogPostForm()
        return render(request, 'blog/blog_form.html', {'form': form})

def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if post.is_draft and post.author != request.user:
        return redirect('home')
    # 渲染Markdown为HTML
    content_html = mark_safe(markdown.markdown(post.content or '', extensions=['fenced_code', 'tables', 'codehilite']))
    # 构造comments上下文，结构与moments一致
    comments = []
    for c in post.comments.all().order_by('-created_at'):
        comments.append({
            'obj': c,
            'liked_by_user': request.user in c.likes.all(),
            'like_count': c.like_count(),
        })
    is_liked = request.user.is_authenticated and (request.user in post.likes.all())
    like_count = post.like_count()
    return render(request, 'blog/blog_detail.html', {
        'post': post,
        'content_html': content_html,
        'comments': comments,
        'user': request.user,
        'is_liked': is_liked,
        'like_count': like_count,
    })

@login_required
def blog_edit(request, blog_id=None):
    if blog_id:
        blog = get_object_or_404(BlogPost, id=blog_id, author=request.user)
    else:
        blog = None
    if request.method == 'POST':
        is_draft = str(request.POST.get('is_draft', '')).lower() in ['true', '1']
        title = request.POST.get('blog_title')
        content = request.POST.get('blog_content') or ''
        category = request.POST.get('category', 'daily')
        blog_tags = request.POST.get('blog_tags')
        blog_summary = request.POST.get('blog_summary')
        publish_to = request.POST.getlist('publish_to')
        publish_type = ','.join(sorted(set([x for x in publish_to if x in ['blog', 'moments', 'plaza', 'private']])))
        cover_image = request.FILES.get('blog_cover')
        if blog:
            blog.title = title
            blog.content = content
            blog.category = category
            blog.blog_tags = blog_tags
            blog.blog_summary = blog_summary
            blog.is_draft = is_draft
            blog.publish_type = publish_type or 'blog'
            if cover_image:
                blog.cover_image = cover_image
            blog.save()
        else:
            blog = BlogPost.objects.create(
                author=request.user,
                title=title,
                content=content,
                category=category,
                blog_tags=blog_tags,
                blog_summary=blog_summary,
                publish_type=publish_type or 'blog',
                cover_image=cover_image,
                is_draft=is_draft,
                is_blog=True,
            )
        if is_draft:
            return redirect('draft_list')
        else:
            return redirect('blog_detail', pk=blog.id)
    if blog and blog.content is None:
        blog.content = ''
    context = {
        'blog': blog,
        'category_choices': CATEGORY_CHOICES,
    }
    return render(request, 'blog/blog_form.html', context)

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
    drafts = BlogPost.objects.filter(author=request.user, is_draft=True).order_by('-last_saved_time')
    return render(request, 'blog/draft_list.html', {'drafts': drafts})

@login_required
def blog_list(request):
    """博客列表页面"""
    blogs = BlogPost.objects.filter(
        is_draft=False,
        is_blog=True,
        author=request.user
    ).order_by('-created_at')
    return render(request, 'blog/blog_list.html', {'blogs': blogs})

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

@csrf_exempt
def upload_blog_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        img = request.FILES['image']
        ext = os.path.splitext(img.name)[-1]
        filename = f'{uuid.uuid4().hex}{ext}'
        save_dir = os.path.join(settings.MEDIA_ROOT, 'blog_imgs')
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, filename)
        with open(save_path, 'wb+') as f:
            for chunk in img.chunks():
                f.write(chunk)
        return JsonResponse({'url': f'/media/blog_imgs/{filename}'})
    return JsonResponse({'error': '上传失败'}, status=400)

@login_required
def create(request):
    if request.method == 'POST':
        content = request.POST.get('blog_content')
        if 'data:image' in content:
            return JsonResponse({'error': '禁止发布 base64 图片，请使用上传功能。'}, status=400)
        if len(content) > 30000:
            return JsonResponse({'error': '内容过长，最多30000字符。'}, status=400)
        # ...原有保存逻辑...

@login_required
def blog_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if post.author != request.user:
        messages.error(request, '你没有权限删除这篇博客。')
        return redirect('blog_detail', pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, '博客已删除。')
        return redirect('blog_list')
    else:
        return redirect('blog_detail', pk=pk)

@require_POST
def like_blog_comment(request, comment_id):
    from .models import BlogComment
    comment = get_object_or_404(BlogComment, id=comment_id)
    user = request.user
    if user in comment.likes.all():
        comment.likes.remove(user)
        liked = False
    else:
        comment.likes.add(user)
        liked = True
    comment.save()
    return JsonResponse({
        'liked': liked,
        'like_count': comment.like_count(),
    })

@require_POST
def delete_blog_comment(request, comment_id):
    from .models import BlogComment
    comment = get_object_or_404(BlogComment, id=comment_id)
    user = request.user
    if comment.author == user or user.is_superuser:
        comment.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': '无权限'}, status=403)

@require_POST
@login_required
def add_blog_comment(request, pk):
    from .models import BlogPost, BlogComment
    post = get_object_or_404(BlogPost, pk=pk)
    content = request.POST.get('comment', '').strip()
    if not content:
        return JsonResponse({'success': False, 'error': '评论内容不能为空'}, status=400)
    comment = BlogComment.objects.create(post=post, author=request.user, content=content)
    c = {
        'obj': comment,
        'liked_by_user': request.user in comment.likes.all(),
        'like_count': comment.like_count(),
    }
    html = render_to_string('blog/_comment_item.html', {'c': c, 'user': request.user}, request=request)
    return JsonResponse({'success': True, 'html': html, 'comment_id': comment.id})

@require_POST
@login_required
def like_blog_post(request, post_id):
    from .models import BlogPost
    post = get_object_or_404(BlogPost, id=post_id)
    user = request.user
    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True
    post.save()
    return JsonResponse({
        'liked': liked,
        'like_count': post.like_count(),
    })

def compress_image(uploaded_file, quality=70, max_size=1024):
    image = Image.open(uploaded_file)
    if max(image.size) > max_size:
        ratio = max_size / max(image.size)
        new_size = (int(image.size[0]*ratio), int(image.size[1]*ratio))
        image = image.resize(new_size, Image.ANTIALIAS)
    output_io = io.BytesIO()
    image = image.convert('RGB')
    image.save(output_io, format='JPEG', quality=quality)
    output_io.seek(0)
    return InMemoryUploadedFile(
        output_io, 'ImageField', uploaded_file.name, 'image/jpeg', output_io.getbuffer().nbytes, None
    )