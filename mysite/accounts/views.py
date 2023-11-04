from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect

menu = [
        {'title': "Новости", 'url_name': 'news'},
        {'title': "О компании", 'url_name': 'about'},
        {'title': "Контакты", 'url_name': 'contacts'},
        {'title': "Регистрация на сайте", 'url_name': 'register'},
        {'title': "Войти на сайт", 'url_name': 'login'},
]
data_db = [
    {'id': 1, 'title': 'Анкерно-угловая опора', 'content': 'Описание А-УО', 'is_published': True},
    {'id': 2, 'title': 'Промежуточная опора', 'content': 'Описание ПО', 'is_published': True},
    {'id': 3, 'title': 'Концевая опора', 'content': 'Описание КО', 'is_published': True},
]
def index(request):
    data = {
        'title': "Главная страница",
        'menu': menu,
        'post': data_db,
    }
    return render(request, 'index.html', context=data)
def news(request):
    data = {'title': "Новости"}
    return render(request, 'news.html', data)
def about(request):
    return render(request, 'about.html', {'title': 'О компании'})
def contacts(request):
    return HttpResponse("<h1>Контакты</h1")
def show_post(request, post_id):
    return HttpResponse(f'Отображение статьи с id = {post_id}')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                return render(request, 'register.html', {'error': 'Username is already taken.'})
            else:
                user = User.objects.create_user(username=username, password=password1)
                user.save()
                return redirect('login')
        else:
            return render(request, 'register.html', {'error': 'Passwords do not match.'})
    else:
        return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials.'})
    else:
        return render(request, 'login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('login')


def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard.html')
    else:
        return redirect('login')