from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_safe, require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Movies
from .forms import MoviesForm

@require_safe
def index(request):
    movies = Movies.objects.order_by('-pk')
    context ={
        'movies' : movies
    }
    return render(request, 'movies/index.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = MoviesForm(request.POST)
        if form.is_valid():
            movie = form.save()
            return redirect('movies:detail', movie.pk)
        
    else:
        form = MoviesForm()
    context = {
        'form': form
    }
    return render(request, 'movies/create.html', context)


@require_safe
def detail(request, movie_pk):
    movie = get_object_or_404(Movies, pk=movie_pk)

    context = {
        'movie': movie,
    }
    return render(request, 'movies/detail.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def update(request, movie_pk):
    movie = get_object_or_404(Movies, pk=movie_pk)

    if request.method == 'POST':
        form = MoviesForm(request.POST, instance=movie)
        if form.is_valid():
            movie = form.save()
            return redirect('movies:detail', movie.pk)
        
    else:
        form = MoviesForm(instance=movie)
    context = {
        'form': form,
        'movie': movie
    }
    return render(request, 'movies/update.html', context)


@login_required
def delete(request, movie_pk):
    if request.method == 'POST':
        movie = get_object_or_404(Movies, pk=movie_pk)
        movie.delete()
    return redirect('movies:index')


@require_safe
def search(request):
    # keyword 가져오기
    keyword = request.GET.get('keyword')
    # keyword가 영화제목에 포함되는 모든 영화들을 가져온다.
    movies = Movies.objects.filter(title__icontains=keyword)
    context = {
        'movies': movies,
    }
    return render(request, 'movies/search.html', context)