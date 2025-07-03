from django.shortcuts import render
import requests
import json
import hashlib
import time
import random
from urllib.parse import urlencode, parse_qs
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.conf import settings
from django.urls import reverse
from .models import QQUser

# QQ OAuth配置
QQ_APP_ID = '102799644'
QQ_APP_KEY = 'JWWP8iBWfhaJtLf0'
QQ_REDIRECT_URI = 'https://app7534.acapp.acwing.com.cn/qq_login/callback'
QQ_AUTHORIZE_URL = 'https://graph.qq.com/oauth2.0/authorize'
QQ_ACCESS_TOKEN_URL = 'https://graph.qq.com/oauth2.0/token'
QQ_OPENID_URL = 'https://graph.qq.com/oauth2.0/me'
QQ_USER_INFO_URL = 'https://graph.qq.com/user/get_user_info'

def qq_login(request):
    """重定向到QQ授权页面"""
    # 生成state参数防止CSRF攻击
    state = hashlib.md5(f"{time.time()}{random.random()}".encode()).hexdigest()
    request.session['qq_state'] = state
    
    # 构建授权URL
    params = {
        'response_type': 'code',
        'client_id': QQ_APP_ID,
        'redirect_uri': QQ_REDIRECT_URI,
        'state': state,
        'scope': 'get_user_info',
    }
    
    authorize_url = f"{QQ_AUTHORIZE_URL}?{urlencode(params)}"
    return redirect(authorize_url)

def qq_callback(request):
    """处理QQ授权回调"""
    # 获取授权码
    code = request.GET.get('code')
    state = request.GET.get('state')
    
    # 验证state参数
    if state != request.session.get('qq_state'):
        return HttpResponse('State验证失败', status=400)
    
    if not code:
        return HttpResponse('授权失败', status=400)
    
    try:
        # 获取access_token
        token_params = {
            'grant_type': 'authorization_code',
            'client_id': QQ_APP_ID,
            'client_secret': QQ_APP_KEY,
            'code': code,
            'redirect_uri': QQ_REDIRECT_URI,
        }
        
        token_response = requests.get(QQ_ACCESS_TOKEN_URL, params=token_params)
        token_data = parse_qs(token_response.text)
        
        if 'error' in token_data:
            return HttpResponse(f'获取access_token失败: {token_data["error"]}', status=400)
        
        access_token = token_data['access_token'][0]
        
        # 获取openid
        openid_params = {
            'access_token': access_token,
        }
        
        openid_response = requests.get(QQ_OPENID_URL, params=openid_params)
        openid_text = openid_response.text
        
        # 解析openid响应（格式：callback( {"client_id":"xxx","openid":"xxx"} );）
        openid_data = json.loads(openid_text.strip('callback( ').rstrip(' );'))
        openid = openid_data['openid']
        
        # 获取用户信息
        user_info_params = {
            'access_token': access_token,
            'oauth_consumer_key': QQ_APP_ID,
            'openid': openid,
        }
        
        user_info_response = requests.get(QQ_USER_INFO_URL, params=user_info_params)
        user_info = user_info_response.json()
        
        if user_info.get('ret') != 0:
            return HttpResponse(f'获取用户信息失败: {user_info.get("msg")}', status=400)
        
        # 查找或创建QQUser
        qq_user = QQUser.objects.filter(qq_openid=openid).first()
        if not qq_user:
            # 创建新用户
            username = f"qq_{openid[:8]}"
            counter = 1
            original_username = username
            while User.objects.filter(username=username).exists():
                username = f"{original_username}_{counter}"
                counter += 1
            user = User.objects.create_user(
                username=username,
                email='',
                password=None  # 不设置密码，因为使用QQ登录
            )
            qq_user = QQUser.objects.create(
                user=user,
                qq_openid=openid,
                qq_nickname=user_info.get('nickname', ''),
                qq_avatar=user_info.get('figureurl_qq_2', user_info.get('figureurl_qq', '')),
            )
        else:
            # 更新现有用户信息
            qq_user.qq_nickname = user_info.get('nickname', qq_user.qq_nickname)
            qq_user.qq_avatar = user_info.get('figureurl_qq_2', user_info.get('figureurl_qq', qq_user.qq_avatar))
            qq_user.save()
            user = qq_user.user
        
        # 登录用户
        login(request, user)
        
        # 清除session中的state
        if 'qq_state' in request.session:
            del request.session['qq_state']
        
        # 重定向到首页
        return redirect('moments:list')
        
    except Exception as e:
        return HttpResponse(f'QQ登录失败: {str(e)}', status=500)
