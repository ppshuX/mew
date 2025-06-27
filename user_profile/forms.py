from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nickname', 'avatar', 'gender', 'birthday', 'location', 'bio']
        widgets = {
            'nickname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your nickname'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control'
            }),
            'birthday': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'YYYY-MM-DD',
                'type': 'date'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City or Region'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Say something about yourself...'
            }),
        }

    # 独立配置 avatar（ImageField），不适合加 form-control 样式
    avatar = forms.ImageField(required=False)
