from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('profile/', views.profile, name='profile'),

    # 1. 회원가입
    # accounts/signup/
    path('signup/', views.signup, name='signup'),

    # 2. 로그인
    # accounts/login/
    path('login/', views.login, name='login'),

    # 3. 로그아웃
    # accounts/logout/
    path('logout/', views.logout, name='logout'),

    # 4. 회원 정보 수정
    # accounts/update/
    path('update/', views.update, name='update'),

    # 5. 비밀 번호 정보 수정
    # accounts/update/
    path('password/', views.password, name='password'),

    # 6. 회원 탈퇴
    path('delete/', views.delete, name='delete'),
]   