from django import forms
from .models import Post

class PlazaPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']