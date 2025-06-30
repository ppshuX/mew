from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.blog_create, name='blog_create'),
    path('<int:pk>/', views.blog_detail, name = 'blog_detail'),
    path('<int:pk>/edit/', views.blog_edit, name='blog_edit'),
]