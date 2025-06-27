from django.urls import path
from . import views

urlpatterns = [
    path('<str:username>/', views.user_profile_detail, name='user_profile_detail'),
    path('<str:username>/edit/', views.user_profile_edit, name='user_profile_edit'),
]