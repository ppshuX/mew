from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Post

class CustomRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    # 自定义密码要求
    def clean_password1(self):
        pwd = self.cleaned_data.get('password1')
        if len(pwd) < 5:
            raise ValidationError("密码至少5位")
        return pwd

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("两次输入的密码不一致")
        return cleaned_data

class MomentsPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'category', 'is_private']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': '想说点什么...'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }
