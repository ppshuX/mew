from django.urls import path
from . import views

urlpatterns = [
    path('', views.moments_list, name='moments'),
    path('<int:post_id>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('<int:post_id>/like/', views.like_post, name='like_post'),
    path('<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
]