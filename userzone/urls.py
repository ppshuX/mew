from django.urls import path
from . import views

app_name = 'userzone'

urlpatterns = [
    path('<str:username>/', views.userzone, name='detail'),
    path('follow/<str:username>/', views.follow_user, name='follow'),
]