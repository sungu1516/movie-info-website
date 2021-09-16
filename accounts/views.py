from django.shortcuts import render, redirect
from django.contrib.auth.forms import (
    ReadOnlyPasswordHashField,
    UserCreationForm,
    AuthenticationForm,
    PasswordChangeForm,
)
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from .forms import CustomUserChangeForm

User = get_user_model()


@require_http_methods(['GET', 'POST'])
def signup(request):
    '''
    GET: 회원가입 템플릿 렌더
    POST: 회원가입 진행 => CREATE
    '''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('movies:index')
    else:
        form = UserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


@require_http_methods(['GET', 'POST'])
def login(request):
    '''
    GET: 로그인 템플릿 렌더
    POST: 로그인 진행
    '''
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'movies:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)



@require_POST
def logout(request):
    '''
    POST: 로그아웃 진행
    '''
    auth_logout(request)
    return redirect('movies:index')


@require_http_methods(['GET', 'POST'])
def update(request):
    '''
    GET: 회원정보 수정 템플릿 렌더
    POST: 회원정보 수정 진행
    '''
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)


@login_required
def profile(request):
    '''
    GET: 프로필 페이지 렌더
    '''
    return render(request, 'accounts/profile.html')


@login_required
def password(request):
    '''
    GET:
    POST:
    '''
    if request.method == 'POST':
        print('POST요청임')
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('accounts:profile')
    else:
        print('POST요청이 아님')
        form = PasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/password_change.html', context)


@login_required
def delete(request):
    if request.method == 'POST':
        request.user.delete()
        auth_logout(request)
        return redirect('accounts:signup')
    return redirect('movies:index')