from django.urls import path
from . import views
from .views import draft_list, simple_create

urlpatterns = [
    path('create/', views.blog_create, name='blog_create'),
    path('<int:pk>/', views.blog_detail, name = 'blog_detail'),
    path('<int:pk>/edit/', views.blog_edit, name='blog_edit'),
    path('drafts/', draft_list, name='blog_draft_list'),
    path('simple_create/', simple_create, name='blog_simple_create'),
]