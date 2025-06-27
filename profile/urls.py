from django.urls import path
from . import views

urlpatterns = [
    path('<str:username>/', views.profile_detail, name='profile_detail'),
    path('<str:username>/edit/', views.profile_edit, name='profile_edit'),
]