from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Post
from captcha.fields import CaptchaField
from captcha.conf import settings as captcha_settings

class CustomRegisterForm(UserCreationForm):
    captcha = CaptchaField(label="验证码")
    email = forms.EmailField(label="邮箱", required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'captcha']

    # 自定义密码要求
    def clean_password1(self):
        pwd = self.cleaned_data.get('password1')
        if len(pwd) < 7:
            raise ValidationError("密码至少7位")
        if pwd.isdigit() or pwd.isalpha():
            raise ValidationError("密码需包含字母和数字的组合")
        return pwd

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("两次输入的密码不一致")
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        from django.contrib.auth.models import User
        if User.objects.filter(email=email).exists():
            raise ValidationError("该邮箱已被注册，请更换邮箱。")
        return email

class LoginForm(forms.Form):
    username = forms.CharField(label="用户名")
    password = forms.CharField(label="密码", widget=forms.PasswordInput)
    def __init__(self, *args, show_captcha=False, **kwargs):
        super().__init__(*args, **kwargs)
        if show_captcha:
            self.fields['captcha'] = CaptchaField(label="验证码", error_messages={
                'invalid': '验证码错误，请重新输入',
                'required': '请输入验证码',
            })

class MomentsPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'category', 'is_private']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': '想说点什么...'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }
