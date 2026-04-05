from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .forms import RegisterForm, LoginForm
from .models import User

import requests


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
    else:
        form = LoginForm(request)
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


def kakao_login(request):
    kakao_auth_url = (
        f"https://kauth.kakao.com/oauth/authorize"
        f"?client_id={settings.KAKAO_REST_API_KEY}"
        f"&redirect_uri={settings.KAKAO_REDIRECT_URI}"
        f"&response_type=code"
    )
    return redirect(kakao_auth_url)


def kakao_callback(request):
    code = request.GET.get('code')
    if not code:
        return redirect('accounts:login')

    token_response = requests.post(
        'https://kauth.kakao.com/oauth/token',
        data={
            'grant_type': 'authorization_code',
            'client_id': settings.KAKAO_REST_API_KEY,
            'client_secret': settings.KAKAO_CLIENT_SECRET,
            'redirect_uri': settings.KAKAO_REDIRECT_URI,
            'code': code,
        },
    )
    token_data = token_response.json()
    access_token = token_data.get('access_token')
    if not access_token:
        return redirect('accounts:login')

    profile_response = requests.get(
        'https://kapi.kakao.com/v2/user/me',
        headers={'Authorization': f'Bearer {access_token}'},
    )
    profile = profile_response.json()

    kakao_id = profile['id']
    nickname = profile.get('properties', {}).get('nickname', '')
    profile_image = profile.get('properties', {}).get('profile_image', '')

    user, created = User.objects.get_or_create(
        kakao_id=kakao_id,
        defaults={
            'username': f'kakao_{kakao_id}',
            'nickname': nickname,
            'profile_image': profile_image,
        },
    )
    if not created:
        user.nickname = nickname
        user.profile_image = profile_image
        user.save(update_fields=['nickname', 'profile_image'])

    login(request, user)
    return redirect('home')
