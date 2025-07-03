from django.urls import path
from . import views

app_name = 'qq_login'

urlpatterns = [
    path('login/', views.qq_login, name='login'),
    path('callback/', views.qq_callback, name='callback'),
] 