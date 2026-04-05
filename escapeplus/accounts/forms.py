from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):
    nickname = forms.CharField(max_length=64, required=False, label='닉네임')
    email = forms.EmailField(required=False, label='이메일')

    class Meta:
        model = User
        fields = ['username', 'nickname', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    pass
