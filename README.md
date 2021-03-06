# Movie-info Website

[toc]

## π»νλ‘μ νΈ μ§νκ³Όμ 

### 1. Model λ§λ€κΈ°

- λͺ©ν 
  - λͺμΈμμ μ‘°κ±΄λλ‘ λͺ¨λΈ ν΄λμ€λ₯Ό λ§λ€κ³ , μ μ ν νλκ°μ μ€μ νλ€.

- μ κ·Ό λ°©μ
  - μ μλ 3κ°μ§ νλ μΈμ `created_at`, `updated_at` νλκ°λ μΆκ°νλ€.
  - λν, `__str__` ν¨μλ₯Ό λ§λ€μ΄ κ°μ²΄λ₯Ό μνλ κ°μΌλ‘ μΆλ ₯νλλ‘ νλ€.
  - λͺ¨λΈ ν΄λμ€ μμ± ν, `makemigrations` μ `migrate` λ₯Ό μμ§ μκ³  μ€μνλ€.

- μ½λ (μΌλΆ)

```python
# models.py

from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    poster_path = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
```



### 2. Urls ν¨ν΄

- λͺ©ν
  - μκ΅¬λλ μμ²­μ μ²λ¦¬νκΈ° μν μ μ ν `urlpatterns` λ₯Ό μμ±νλ€.

- μ κ·Ό λ°©μ
  - νλ‘μ νΈ λλ ν λ¦¬ νμ urls.py μ `include` λ©μλλ₯Ό νμ©νμ¬, movieμ κ΄λ ¨λ μμ²­μ λͺ¨λ movies μ΄νλ¦¬μΌμ΄μ νμ urls.py μμ μ²λ¦¬λ  μ μλλ‘ νλ€.
  - μ΄νλ¦¬μΌμ΄μμ urls.py μ κΈ°λ₯λ³(CRUD)λ‘ κ΅¬λΆνμ¬ urlspatterns λ₯Ό μμ±ν΄μ€λ€. views μμ νΉμ  ν¨μμ λ―Έλ¦¬ μ°κ²°ν΄μ£Όκ³ , νΈμλ₯Ό μν΄ app_nameκ³Ό urlλ³ name μ μ§μ ν΄μ€λ€.

- μ½λ

```python
# urls (pjt05)

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('movies/', include('movies.urls')),
]

# urls (movies)

from django.urls import path
from . import views

# νμ₯μ±μ μν΄ app_name μ μ§μ 
app_name = 'movies'

# movies/~~
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
```



### 3. View & Template λ§λ€κΈ°

#### 1) κ³΅μ  ννλ¦Ώ μμ±

- λͺ©ν
  - λͺ¨λ  ννλ¦Ώμ μμμ ν΅μΌνκΈ° μν΄ base.html μ λ§λ­λλ€.

- μ κ·Ό λ°©μ
  - `blok` μ μ΄μ©νμ¬ κ°λ³ template μ΄ κ°μ§ λ΄μ©μ λ£μ΄μ£Όκ³ , κ·Έ μ΄μΈμ λΆλΆμ ν΅μΌνλ€.
  - bootstrap μ νμ©νλ€. 
  - nav λ₯Ό λ§λ€κ³ , a νκ·Έλ₯Ό μ΄μ©νμ¬ μ μ ν urlλ‘ μ΄λνλλ‘ νλ€.

- μ½λ

```python
# base.html

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-F3w7mX95PdgyTmZZMECAngseQB83DfGTowi0iMjiWaeVhAn4FJkqJByhZMI3AhiU" crossorigin="anonymous">
  <title>Document</title>
</head>
<body>
  <div class="container">
  
  {% include '_navbar.html' %}
  {% block content %}
  {% endblock content %}
  </div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/js/bootstrap.bundle.min.js" integrity="sha384-/bQdsTh/da6pkI1MST/rWKFNjaCP5gBSY4sEBT38Q/9RBh9AH40zEOg7Hlq2THRZ" crossorigin="anonymous"></script>
</body>
</html>


# _navbar.html

<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <div class="container-fluid">
    <a class="navbar-brand text-primary" href="{% url 'movies:index' %}">Home</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
          <a class="nav-link active text-danger" aria-current="page" href="{% url 'movies:create' %}">Create</a>
        </li>
      </ul>
          <div class="mt-2 me-5">
    <form class="d-flex" action="{% url 'movies:search' %}">
      <input class="form-control me-2" type="search" placeholder="μ λͺ©μ μλ ₯νμΈμ" aria-label="Search" name="keyword" required>
      <button class="btn btn-outline-success" type="submit">Search</button>
    </form>
  </div>
    </div>
  </div>

</nav>
```





#### 2) Read - μ μ²΄ μν λͺ©λ‘ μ‘°ν & λ¨μΌμν μμΈμ‘°ν

- λͺ©ν
  - μ μ²΄ μν λͺ©λ‘μ κ°μ Έμ νλ©΄μ νμν  μ μλλ‘ views μ ν¨μλ₯Ό μ μνκ³ , template λ₯Ό λ§λ λ€.
  - νΉμ  μνμ μ λͺ©μ ν΄λ¦­νλ©΄ μμΈ μ λ³΄κ° νλ©΄μ νμλλλ‘ κ΅¬ννλ€.

- μ κ·Ό λ°©μ
  - READ κΈ°λ₯μ ν  μ μλ index ν¨μμ detail ν¨μλ₯Ό μ μνλ€.
  - `index` ν¨μμ κ²½μ°, `order_by()` λ₯Ό μ¬μ©ν΄ λͺ¨λ  μνμ λ³΄κ° pkλ₯Ό κΈ°μ€μΌλ‘ λ΄λ¦Όμ°¨μ μ λ ¬ λλλ‘ νλ€. 
  - `detail` ν¨μμ κ²½μ° λκ²¨λ°μ movie_pk λ₯Ό μ΄μ©ν΄ ν΄λΉ μνμ λ³΄λ₯Ό νλ©΄μ λ λνλ€.

- μ½λ

```python
# views.py

@require_safe
def index(request):
    movies = Movies.objects.order_by('-pk')
    context ={
        'movies' : movies
    }
    return render(request, 'movies/index.html', context)

@require_safe
def detail(request, movie_pk):
    movie = get_object_or_404(Movies, pk=movie_pk)

    context = {
        'movie': movie,
    }
    return render(request, 'movies/detail.html', context)
```





#### 3) Create - μλ‘μ΄ μν μμ± Form & μν λ°μ΄ν° μ μ₯

- λͺ©ν
  - μ¬μ©μκ° μνμ λ³΄λ₯Ό μλ‘­κ² μλ ₯ν  μ μλ form νλ©΄μ λ λλ§νλ€.
  - μλ ₯λ°μ μν μ λ³΄λ₯Ό DBμ μ μ₯νλ€.

- μ κ·Ό λ°©μ
  - views.py μ CREATE κΈ°λ₯μ ν  μ μλ`create` ν¨μλ₯Ό λ§λ λ€.
  - create ν¨μμ κ²½μ°, μμ²­μ΄ GETμΌλ‘ μλμ§ νΉμ POSTλ‘ μλμ§μ λ°λΌ λ€λ₯Έ μλ΅μ λ³΄λ΄λλ‘ νλ€.
  - POST μμ²­ μ, λκ²¨μ€ λ°μ΄ν°λ₯Ό κ°μ Έμ DBμ μ μ₯ν΄μ€λ€.
  
- μ½λ

```python
# views.py

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
```





#### 4) Update - μμ ν  μν μ λ³΄κ° λ΄κΈ΄ μμ  form & μμ ν μνλ°μ΄ν° μ μ₯

- λͺ©ν
  - μ¬μ©μκ° κΈ°μ‘΄μ κ²μκΈμ μμ ν  μ μλ form νλ©΄μ λ λλ§νλ€.
  - μμ ν μν μ λ³΄λ₯Ό DBμ μ μ₯νλ€.
- μ κ·Ό λ°©μ
  - μμ  λ²νΌμ detail νμ΄μ§μ λ§λ€μ΄μ€λ€.
  - views.py μ UPDATE κΈ°λ₯μ ν  μ μλ  `update` ν¨μλ₯Ό λ§λ λ€.
  - κΈ°μ‘΄μ λ΄μ©μ κ·Έλλ‘ μ μ§ν΄μΌ νκΈ° λλ¬Έμ, movie.pk λ₯Ό νμ©νλ€.
  - update ν¨μ μ­μ create μ μ μ¬νκ², μμ²­ λ°©μμ λ°λΌ λ€λ₯Έ μλ΅ κ²°κ³Όλ₯Ό λ°ννλλ‘ νλ€.
- μ½λ

```python
# views.py

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
```





#### 5) Delete - μνμ λ³΄λ₯Ό μ­μ 

- λͺ©ν
  - νΉμ  μνμ λ³΄λ₯Ό μ­μ νλ κΈ°λ₯μ κ΅¬ννλ€.
- μ κ·Ό λ°©μ
  - μ­μ  λ²νΌμ detail νμ΄μ§μ λ§λ€μ΄μ€λ€.
  - detail νμ΄μ§μ μ­μ λ²νΌμ λ§λ€ μ, a νκ·Έκ° μλ form νκ·Έλ‘ μμ±νμ¬ POST μμ²­μ νλλ‘ νλ€. μ΄λ detail νμ΄μ§μμ μ­μ λ²νΌμ λλ¬ μ­μ μμ²­μμλ§ μνμ λ³΄κΈμ΄ μ§μμ§λλ‘ νκΈ° μν¨μ΄λ€.
  - delete ν¨μλ₯Ό λ§λ€κ³ , μ‘°κ±΄λ¬Έμ νμ©ν΄ λ§μ½ μμ²­λ°©λ²μ΄ POST μΌ λλ§ DBμ λ°μ΄ν°λ₯Ό μ­μ νλ€. λ§μ½ GET λ°©μμΌλ‘ μ­μ  μμ²­ν  κ²½μ°, μ­μ νμ§ μκ³  detail νμ΄μ§λ‘ λ€μ λμκ°λ€.
- μ½λ

```python
# views.py

@require_POST
def delete(request, movie_pk):
    movie = get_object_or_404(Movies, pk=movie_pk)
    movie.delete()
    return redirect('movies:index')
```





#### 6) μΆκ°κΈ°λ₯ - Search

- λͺ©ν
  - κ²μ keyword κ° ν¬ν¨λ μν λͺ©λ‘μ νλ©΄μ νμνλ€.

- μ κ·Ό λ°©μ
  - search ν¨μλ₯Ό μ μνκ³ , filter μ νμ©νμ¬ μνλ μ‘°κ±΄μ μνλ€μ κ°μ Έμ΅λλ€.
  - νΉμ  κΈμκ° ν¬ν¨λ κ²°κ³Όλ₯Ό κ°μ Έμ€κΈ° μν΄ `__icontains` λ₯Ό νμ©νλ€.
  - context λ₯Ό search ννλ¦ΏμΌλ‘ λλ €μ£Όκ³ , search.html μμ ν΄λΉ μνλ€μ νμνλ€.


- μ½λ

```python
# views

def search(request):
    # keyword κ°μ Έμ€κΈ°
    keyword = request.GET.get('keyword')
    # keywordκ° μνμ λͺ©μ ν¬ν¨λλ λͺ¨λ  μνλ€μ κ°μ Έμ¨λ€.
    movies = Movie.objects.filter(title__icontains=keyword)
    context = {
        'movies': movies,
    }
    return render(request, 'movies/search.html', context)
```





## :book: νμ΅ν λ΄μ©

### 1. POSTμ GETμ μ°¨μ΄

- POST μ GETμ λͺνν μ°¨μ΄λ₯Ό μκ² λμλ€.
- GETμ λ°μ΄ν°λ₯Ό κ°μ Έμ€κΈ°λ§ ν  λ, POSTλ λ°μ΄ν°λ₯Ό μμ  λ° μ­μ ν  λ νμ©λ  μ μλ€.
- λν, νΉμ  λ²νΌμ λλ Έμ λ POST λ°©μμΌλ‘ μμ²­μ΄ κ°λλ‘ νλ κ΅¬ν λ°©λ²λ μκ² λμλ€.



### 2. Search κΈ°λ₯ κ΅¬ν λ°©λ² 

- μΆκ° κΈ°λ₯μΈ Search κΈ°λ₯μ κ΅¬ν λ°©λ²μ λν΄μλ μκ² λμλ€.
- searchμ κ²½μ° μ λ³΄λ₯Ό κ°μ Έμ μ‘°μνλ κ²μ΄ μλκΈ° λλ¬Έμ, get λ°©μμΌλ‘ μμ²­ κ°λ₯νλ€.
- νΉμ  ν€μλκ° ν¬ν¨λλκ°μ λν κ²°κ³Όλ₯Ό μκΈ° μν΄μλ `filter`, `__icontains` λ₯Ό νμ©ν  μ μλ€.



### 3. κ΄λ¦¬μ νμ΄μ§ νμ©λ°©λ²

```python
# admin.py

from django.contrib import admin
from .models import Movie

admin.site.register(Movie)

# bash λͺλ Ή
$ python manage.py createsuperuser
```

- κ΄λ¦¬μ νμ΄μ§μ κ³μ μ λ§λ€κ³ , νμ΄μ§μμ μ§μ  λ°μ΄ν°λ₯Ό λ£λ λ°©λ²μ λ°°μΈ μ μμλ€.
- μ΄λ°μ λ°μ΄ν°λ‘ μ¬λ¬ μλλ₯Ό νκ³  μΆμλ° shell_plus λ₯Ό μν extentions μ΄ μ€μΉλμ΄ μμ§ μμ κ²½μ°, λ°μ΄ν°λ₯Ό μμ½κ² DB μ λ£κΈ°μ μ’μ κ² κ°λ€.



## :thinking:λλμ 

- μ΄μ μ homework, workshopμ λͺλ² ν΄λ΄μμΈμ§, κΈ°λ³Έμ μΈ κΈ°λ₯μ κ΅¬ννλ κ²μ κ·Έλ¦¬ μ΄λ ΅μ§ μμλ€!! μ­μ λ§μ μ€μ΅κ³Ό μ°μ΅, λ°λ³΅μ΄ μ€μνλ€κ³  λκΌλ€.
- μ΄μ μ νλ‘ νΈλ‘ νλ νλ‘μ νΈλ³΄λ€ ν¨μ¬ μ¬λ°λ€κ³  λκ»΄μ‘λ€. μ§μ  λ°μ΄ν°λ₯Ό μ μ₯νκ³ , κ°μ Έμ μμ νκ³  κ²°κ³Όλ₯Ό νλ©΄μ νννλ κ³Όμ μ΄ μ¬λ―Έμμκ³ , κ²°κ³Όλ₯Ό λ³΄λ λΏλ―νλ€.



### β 1. μ΄λ €μ λ μ 

- μ­μ CSS κ° λ³΅λ³μ΄μλ€... μνλ λλ‘ κΉλνκ² νλ©΄μ κ΅¬μ±νλ κ²μ΄ μ΄λ €μ λ€. νΉν μν λͺ©λ‘μ μΉ΄λ νμμΌλ‘ λ³΄μ¬μ£Όκ³ μ ν  λ, django μ forλ¬Έ μμμ μ λ ¬μ μλν΄μ μ λ₯Ό λ¨Ήμλ€....

- search κΈ°λ₯μ λ§μ΄ μ°μ΅ν΄λ³΄μ§ μμμ κ΅¬ννλ κ²μ΄ μν΄λ λ€. μ΅νλλ‘ νμ!!



## μλ°μ΄νΈ (09.16)

- accounts app μΆκ°
- νμκ°μ, λ‘κ·ΈμΈ & λ‘κ·Έμμ κΈ°λ₯ μΆκ°
- νμμ λ³΄ νμΈ λ° μμ  & μ­μ  κΈ°λ₯ μΆκ° 
- Bootstrapμ νμ©ν΄ UI κ°μ 
- νμμ΄ μλ κ²½μ° κΈ μμ± λ° μμ , μ­μ κ° λΆκ°λ₯νκ² ν¨
