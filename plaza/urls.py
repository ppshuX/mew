from django.urls import path
from . import views

app_name = 'plaza'

urlpatterns = [
    path('', views.plaza_list, name='list'),
    path('<int:post_id>/', views.plaza_detail, name='detail'),
    path('<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('<int:post_id>/like/', views.like_post, name='like_post'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('comment/<int:comment_id>/like/', views.like_comment, name='like_comment'),
    path('<int:post_id>/delete/', views.delete_post, name='delete_post'),
]
