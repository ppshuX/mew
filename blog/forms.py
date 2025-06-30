from django import forms
from .models import BlogPost

PUBLISH_CHOICES = [
    ('private', '私密动态'),
    ('moments', '朋友圈'),
    ('plaza', '广场'),
]

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['content', 'title', 'cover_image', 'category', 'publish_type', 'blog_tags', 'blog_summary']

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
    
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'mew-form-input', 'placeholder': '标题（可选）'}),
        required=False
    )
    content = forms.CharField(
        max_length=5000,
        widget=forms.Textarea(attrs={'class': 'mew-form-textarea', 'placeholder': '写下你的动态内容……', 'rows': 6}),
        required=True
    )
    cover_image = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'mew-form-input'}),
        required=False
    )
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'mew-form-select'}),
        required=False,
        initial='daily'
    )
    publish_type = forms.ChoiceField(
        choices=PUBLISH_CHOICES,
        widget=forms.Select(attrs={'class': 'mew-form-select'}),
        initial='private',
        label='发布到'
    )
    blog_tags = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'mew-form-input', 'placeholder': '如：技术,生活,随笔'})
    )
    blog_summary = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.Textarea(attrs={'class': 'mew-form-textarea', 'placeholder': '一句话介绍你的博客', 'rows': 2})
    )