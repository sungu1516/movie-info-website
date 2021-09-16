from django.urls import path
from . import views


app_name = 'movies'
urlpatterns = [
    # ~/movies/create/
    path('create/', views.create, name='create'),
    # ~/movies/
    path('', views.index, name='index'),
    # ~/movies/<pk>/
    path('<int:movie_pk>/', views.detail, name='detail'),
    # ~/movies/<pk>/update/
    path('<int:movie_pk>/update', views.update, name='update'),
    # ~/movies/<pk>/delete/
    path('<int:movie_pk>/delete/', views.delete, name='delete'),
    # ~/movies/search/
    path('search/', views.search, name='search'),
]
