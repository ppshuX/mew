from django.urls import path
from . import views

app_name = 'moments'

urlpatterns = [
    path('', views.moments_list, name='list'),
    path('<int:post_id>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('<int:post_id>/like/', views.like_post, name='like_post'),
    path('<int:post_id>/delete/', views.delete_post, name='delete_post'),

    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('comment/<int:comment_id>/like/', views.like_comment, name='like_comment'),
]