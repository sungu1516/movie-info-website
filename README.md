# Movie-info Website

[toc]

## 💻프로젝트 진행과정

### 1. Model 만들기

- 목표 
  - 명세서의 조건대로 모델 클래스를 만들고, 적절한 필드값을 설정한다.

- 접근 방식
  - 제시된 3가지 필드 외에 `created_at`, `updated_at` 필드값도 추가한다.
  - 또한, `__str__` 함수를 만들어 객체를 원하는 값으로 출력하도록 한다.
  - 모델 클래스 생성 후, `makemigrations` 와 `migrate` 를 잊지 않고 실시한다.

- 코드 (일부)

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



### 2. Urls 패턴

- 목표
  - 요구되는 요청을 처리하기 위한 적절한 `urlpatterns` 를 작성한다.

- 접근 방식
  - 프로젝트 디렉토리 하의 urls.py 엔 `include` 메서드를 활용하여, movie와 관련된 요청은 모두 movies 어플리케이션 하의 urls.py 에서 처리될 수 있도록 한다.
  - 어플리케이션의 urls.py 에 기능별(CRUD)로 구분하여 urlspatterns 를 작성해준다. views 안의 특정 함수와 미리 연결해주고, 편의를 의해 app_name과 url별 name 을 지정해준다.

- 코드

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

# 확장성을 위해 app_name 을 지정
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



### 3. View & Template 만들기

#### 1) 공유 템플릿 생성

- 목표
  - 모든 템플릿의 양식을 통일하기 위해 base.html 을 만듭니다.

- 접근 방식
  - `blok` 을 이용하여 개별 template 이 가질 내용을 넣어주고, 그 이외의 부분은 통일한다.
  - bootstrap 을 활용한다. 
  - nav 를 만들고, a 태그를 이용하여 적절한 url로 이동하도록 한다.

- 코드

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
      <input class="form-control me-2" type="search" placeholder="제목을 입력하세요" aria-label="Search" name="keyword" required>
      <button class="btn btn-outline-success" type="submit">Search</button>
    </form>
  </div>
    </div>
  </div>

</nav>
```





#### 2) Read - 전체 영화 목록 조회 & 단일영화 상세조회

- 목표
  - 전체 영화 목록을 가져와 화면에 표시할 수 있도록 views 의 함수를 정의하고, template 를 만든다.
  - 특정 영화의 제목을 클릭하면 상세 정보가 화면에 표시되도록 구현한다.

- 접근 방식
  - READ 기능을 할 수 있는 index 함수와 detail 함수를 정의한다.
  - `index` 함수의 경우, `order_by()` 를 사용해 모든 영화정보가 pk를 기준으로 내림차순 정렬 되도록 한다. 
  - `detail` 함수의 경우 넘겨받은 movie_pk 를 이용해 해당 영화정보를 화면에 렌더한다.

- 코드

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





#### 3) Create - 새로운 영화 작성 Form & 영화 데이터 저장

- 목표
  - 사용자가 영화정보를 새롭게 입력할 수 있는 form 화면을 렌더링한다.
  - 입력받은 영화 정보를 DB에 저장한다.

- 접근 방식
  - views.py 에 CREATE 기능을 할 수 있는`create` 함수를 만든다.
  - create 함수의 경우, 요청이 GET으로 왔는지 혹은 POST로 왔는지에 따라 다른 응답을 보내도록 한다.
  - POST 요청 시, 넘겨준 데이터를 가져와 DB에 저장해준다.
  
- 코드

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





#### 4) Update - 수정할 영화 정보가 담긴 수정 form & 수정한 영화데이터 저장

- 목표
  - 사용자가 기존의 게시글을 수정할 수 있는 form 화면을 렌더링한다.
  - 수정한 영화 정보를 DB에 저장한다.
- 접근 방식
  - 수정 버튼을 detail 페이지에 만들어준다.
  - views.py 에 UPDATE 기능을 할 수 있는  `update` 함수를 만든다.
  - 기존의 내용을 그대로 유지해야 하기 때문에, movie.pk 를 활용한다.
  - update 함수 역시 create 와 유사하게, 요청 방식에 따라 다른 응답 결과를 반환하도록 한다.
- 코드

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





#### 5) Delete - 영화정보를 삭제

- 목표
  - 특정 영화정보를 삭제하는 기능을 구현한다.
- 접근 방식
  - 삭제 버튼을 detail 페이지에 만들어준다.
  - detail 페이지에 삭제버튼을 만들 시, a 태그가 아닌 form 태그로 작성하여 POST 요청을 하도록 한다. 이는 detail 페이지에서 삭제버튼을 눌러 삭제요청시에만 영화정보글이 지워지도록 하기 위함이다.
  - delete 함수를 만들고, 조건문을 활용해 만약 요청방법이 POST 일 때만 DB의 데이터를 삭제한다. 만약 GET 방식으로 삭제 요청할 경우, 삭제하지 않고 detail 페이지로 다시 돌아간다.
- 코드

```python
# views.py

@require_POST
def delete(request, movie_pk):
    movie = get_object_or_404(Movies, pk=movie_pk)
    movie.delete()
    return redirect('movies:index')
```





#### 6) 추가기능 - Search

- 목표
  - 검색 keyword 가 포함된 영화 목록을 화면에 표시한다.

- 접근 방식
  - search 함수를 정의하고, filter 을 활용하여 원하는 조건의 영화들을 가져옵니다.
  - 특정 글자가 포함된 결과를 가져오기 위해 `__icontains` 를 활용한다.
  - context 를 search 템플릿으로 넘려주고, search.html 에서 해당 영화들을 표시한다.


- 코드

```python
# views

def search(request):
    # keyword 가져오기
    keyword = request.GET.get('keyword')
    # keyword가 영화제목에 포함되는 모든 영화들을 가져온다.
    movies = Movie.objects.filter(title__icontains=keyword)
    context = {
        'movies': movies,
    }
    return render(request, 'movies/search.html', context)
```





## :book: 학습한 내용

### 1. POST와 GET의 차이

- POST 와 GET의 명확한 차이를 알게 되었다.
- GET은 데이터를 가져오기만 할 때, POST는 데이터를 수정 및 삭제할 때 활용될 수 있다.
- 또한, 특정 버튼을 눌렸을 때 POST 방식으로 요청이 가도록 하는 구현 방법도 알게 되었다.



### 2. Search 기능 구현 방법 

- 추가 기능인 Search 기능의 구현 방법에 대해서도 알게 되었다.
- search의 경우 정보를 가져와 조작하는 것이 아니기 때문에, get 방식으로 요청 가능하다.
- 특정 키워드가 포함되는가에 대한 결과를 알기 위해서는 `filter`, `__icontains` 를 활용할 수 있다.



### 3. 관리자 페이지 활용방법

```python
# admin.py

from django.contrib import admin
from .models import Movie

admin.site.register(Movie)

# bash 명령
$ python manage.py createsuperuser
```

- 관리자 페이지의 계정을 만들고, 페이지에서 직접 데이터를 넣는 방법을 배울 수 있었다.
- 초반에 데이터로 여러 시도를 하고 싶은데 shell_plus 를 위한 extentions 이 설치되어 있지 않은 경우, 데이터를 손쉽게 DB 에 넣기에 좋은 것 같다.



## :thinking:느낀점

- 이전에 homework, workshop을 몇번 해봐서인지, 기본적인 기능을 구현하는 것은 그리 어렵지 않았다!! 역시 많은 실습과 연습, 반복이 중요하다고 느꼈다.
- 이전에 프론트로 했던 프로젝트보다 훨씬 재밌다고 느껴졌다. 직접 데이터를 저장하고, 가져와 수정하고 결과를 화면에 표현하는 과정이 재미있었고, 결과를 보니 뿌듯했다.



### ⁉ 1. 어려웠던 점

- 역시 CSS 가 복병이었다... 원하는 대로 깔끔하게 화면을 구성하는 것이 어려웠다. 특히 영화 목록을 카드 형식으로 보여주고자 할 때, django 의 for문 안에서 정렬을 시도해서 애를 먹었다....

- search 기능은 많이 연습해보지 않아서 구현하는 것이 서툴렀다. 익히도록 하자!!



## 업데이트 (09.16)

- accounts app 추가
- 회원가입, 로그인 & 로그아웃 기능 추가
- 회원정보 확인 및 수정 & 삭제 기능 추가 
- Bootstrap을 활용해 UI 개선
- 회원이 아닌 경우 글 작성 및 수정, 삭제가 불가능하게 함
