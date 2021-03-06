from django import forms
from django.contrib import auth
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名'}))
    code = forms.CharField(label='邀请码',
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入邀请码'}))
    password = forms.CharField(label='密码', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}))
    password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请确认密码'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('该用户名已存在')
        return username

    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('两次密码输入不一致')
        return password2


class AuthForm(forms.Form):
    username = forms.CharField(label='用户名', widget=forms.TextInput())
    password = forms.CharField(label='密码', widget=forms.PasswordInput())

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('用户名或密码错误')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data
