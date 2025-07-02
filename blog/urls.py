from django.urls import path
from . import views
from .views import draft_list, simple_create, upload_blog_image

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('create/', views.blog_create, name='blog_create'),
    path('<int:pk>/', views.blog_detail, name = 'blog_detail'),
    path('simple_create/', simple_create, name='blog_simple_create'),
    path('api/upload_blog_image/', upload_blog_image, name='upload_blog_image'),
    path('new/', views.blog_edit, name='blog_new'),
    path('<int:blog_id>/edit/', views.blog_edit, name='edit_blog'),
    path('drafts/', views.draft_list, name='draft_list'),
    path('<int:pk>/delete/', views.blog_delete, name='blog_delete'),
    path('comment/<int:comment_id>/like/', views.like_blog_comment, name='like_blog_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_blog_comment, name='delete_blog_comment'),
    path('<int:pk>/add_comment/', views.add_blog_comment, name='add_blog_comment'),
    path('<int:post_id>/like/', views.like_blog_post, name='like_blog_post'),
]