"""
URL configuration for mew project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from moments import views as custom_views
from django.contrib.auth.views import LogoutView
from captcha.fields import CaptchaField
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', lambda request: redirect('chat/', permanent=False)),
    path('chat/', include('chat.urls')),
    path('moments/', include('moments.urls')),
    path('user_profile/', include('user_profile.urls')),
    path('plaza/', include('plaza.urls')),
    path('userzone/', include('userzone.urls')),
    path('blog/', include('blog.urls')),
    path('admin/', admin.site.urls),

    path('accounts/login/', custom_views.login_view, name='login'),
    path('accounts/logout/', LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),
    path('accounts/register/', custom_views.register, name='register'),
    path('accounts/activate/<uidb64>/<token>/', custom_views.activate_account, name='activate_account'),
    path('qq_login/', include('qq_login.urls')),
    path('captcha/', include('captcha.urls')),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
]

# 添加静态文件和媒体文件的URL配置
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
