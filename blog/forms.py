from django import forms
from .models import BlogPost

PUBLISH_CHOICES = [
    ('private', '私密动态'),
    ('moments', '朋友圈'),
    ('plaza', '广场'),
]

class BlogPostForm(forms.Form):
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
        max_length=500,
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