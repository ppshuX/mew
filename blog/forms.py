from django import forms
from .models import BlogPost

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'cover_image', 'content', 'category', 'is_draft']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '标题'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '写下你的博客内容……'}),
            'category': forms.TextInput(attrs={'class': 'form-control','placeholder': '分类'}),
        }