from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.urls import reverse
from access.forms import AuthForm, RegisterForm
from access.utils import get_status, post_cmd, judg_c_time, judg_s_time

User = get_user_model()


def register(request):
    if request.method == 'POST':
        user_reg_form = RegisterForm(request.POST)
        if user_reg_form.is_valid():
            cd = user_reg_form.cleaned_data
            username = cd['username']
            password = cd['password']
            code = cd['code']
            user = User()
            user.username = username
            user.set_password(password)
            if code == 'hfTwhvi6':
                user.is_student = True
            elif code == '6Wwhzt9M':
                user.is_teacher = True
            elif code == 'CcME3Q3Y':
                user.is_cleaner = True
            user.save()
            return redirect(reverse('index', args=[]))
    else:
        user_reg_form = RegisterForm()
    context = dict()
    context['user_reg_form'] = user_reg_form
    return render(request, 'register.html', context)


def logout(request):
    auth.logout(request)
    return redirect(reverse('index'))


def index(request):
    if request.user.is_authenticated:
        return redirect(reverse('pre_open_door'))
    else:
        if request.method == 'POST':
            authform = AuthForm(request.POST)
            if authform.is_valid():
                cd = authform.cleaned_data
                user = cd['user']
                auth.login(request, user)
                return redirect(reverse('pre_open_door', args=[]))
        else:
            authform = AuthForm()
        context = dict()
        context['authform'] = authform
        return render(request, 'index.html', context)


def pre_opendoor(request):
    user = request.user
    status = get_status()
    context = dict()
    if User.objects.filter(username=user.username).exists():
        if user.is_student:
            # 学生
            if judg_s_time():
                status = get_status()
            else:
                context['error_msg'] = '无权限'

        elif user.is_cleaner:
            # 清洁人员
            if judg_c_time():
                status = get_status()
            else:
                context['error_msg'] = '不在正确时间'
        context['status'] = status
    return render(request, 'pre_opendoor.html', context)


def opdoor(request):
    res = post_cmd(1)
    context = res
    return HttpResponse('%s' % context)

