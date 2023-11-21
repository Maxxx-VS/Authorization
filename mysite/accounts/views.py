from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from .forms import RegistrationForm
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Task
import os
from PIL import Image

flag = False
menu = [
        {'title': "Новости", 'url_name': 'news'},
        {'title': "О компании", 'url_name': 'about'},
        {'title': "Контакты", 'url_name': 'contacts'},
        {'title': "To-Do List", 'url_name': 'task_list'},
        {'title': "Готовим вместе", 'url_name': 'cooking'},
        {'title': "Блог автора", 'url_name': 'blog'},
        {'title': "Регистрация на сайте", 'url_name': 'register'},
        {'title': "Войти на сайт", 'url_name': 'login'},
        {'title': "Обработка изображений", 'url_name': 'process_image'},
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
    return render(request, 'about.html', {'title': 'О компании', 'menu': menu})
def contacts(request):
    return HttpResponse("<h1>Контакты</h1")
def show_post(request, post_id):
    return HttpResponse(f'Отображение статьи с id = {post_id}')

def cooking(request):
    return render(request, "cooking.html")
def plov(request, portion):
    return HttpResponse(f"<h1>Вы готовите ПЛОВ на {portion} порций</h1>"
                        f"<li>Мясо {int(2 * portion)} кг. </li>"
                        f"<li>Рис {int(3 * portion)} кг. </li>"
                        f"<li>Морковь {int(1 * portion)} кг. </li>"
                        f"<li>Лук {int(1 * portion)} кг. </li>")
def soup(request, portion):
    return HttpResponse(f"<h1>Вы готовите СУП на {portion} порций</h1>"
                        f"<li>Картошка {int(3 * portion)} кг. </li>"
                        f"<li>Макароны {int(2 * portion)} кг. </li>"
                        f"<li>Морковь {int(4 * portion)} кг. </li>"
                        f"<li>Лук {int(6 * portion)} кг. </li>")
def porridge(request, portion):
    return HttpResponse(f"<h1>Вы готовите КАШУ на {portion} порций</h1>"
                        f"<li>Мясо {int(4 * portion)} кг. </li>"
                        f"<li>Рис {int(5 * portion)} кг. </li>"
                        f"<li>Морковь {int(3 * portion)} кг. </li>"
                        f"<li>Лук {int(2 * portion)} кг. </li>")

@csrf_exempt
def blog(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            save_to_file(username, password)
            return render(request, 'registration_success.html')
    else:
        form = RegistrationForm()
    return render(request, 'blog.html', {'form': form})

def save_to_file(username, password):
    file_path = settings.USER_DATA_FILE
    with open(file_path, 'a') as file:
        file.write(f"Username: {username}, Publish: {password}\n")


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                return render(request, 'register.html', {'error': 'Имя пользователя уже занято.'})
            else:
                user = User.objects.create_user(username=username, password=password1)
                user.save()
                return redirect('login')
        else:
            return render(request, 'register.html', {'error': 'Пароли не совпадают.'})
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
            return render(request, 'login.html', {'error': 'Неверные учетные данные.'})
    else:
        return render(request, 'login.html')
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('login')
def dashboard(request):
    global flag
    if request.user.is_authenticated:
        flag = True
        return render(request, 'dashboard.html')
    else:
        return redirect('login')

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})

# добавить проверку на флаг
def add_task(request):
    global flag
    if flag:
        if request.method == 'POST':
            title = request.POST['title']
            task = Task.objects.create(title=title)
            return redirect('task_list')
    else:
        return redirect('task_list')
def delete_task(request, task_id):
    global flag
    if flag:
        Task.objects.get(id=task_id).delete()
        return redirect('task_list')
    else:
        return redirect('task_list')
def edit_task(request, task_id):
    global flag
    if flag:
        task = Task.objects.get(id=task_id)
        if request.method == 'POST':
            title = request.POST['title']
            task.title = title
            task.save()
            return redirect('task_list')
        return render(request, 'edit_task.html', {'task': task})
    else:
        return redirect('task_list')

def DarkFilter(r: int, g: int, b: int) -> tuple[int, int, int]:
    result = []
    for color in (r, g, b):
        result = [int(r/3), int(g/3), int(b/3)]
    return tuple(result)
def BrightFilter(r: int, g: int, b: int) -> tuple[int, int, int]:
    result = []
    for color in (r, g, b):
        result = [int(r*3), int(g*3), int(b*3)]
    return tuple(result)

def RedFilter(r: int, g: int, b: int) -> tuple[int, int, int]:
    result = []
    for color in (r, g, b):
        result = [int(r*3), int(g*1), int(b*1)]
    return tuple(result)

def GreenFilter(r: int, g: int, b: int) -> tuple[int, int, int]:
    result = []
    for color in (r, g, b):
        result = [int(r*1), int(g*3), int(b*1)]
    return tuple(result)

def BlueFilter(r: int, g: int, b: int) -> tuple[int, int, int]:
    result = []
    for color in (r, g, b):
        result = [int(r*1), int(g*1), int(b*3)]
    return tuple(result)

def Drugs_eye(r: int, g: int, b: int) -> tuple[int, int, int]:
    result = []
    if r == 90 and g == 141 and b == 61:
        result = [int(randrange(25, 250)), int(randrange(25, 250)), int(randrange(25, 250))]
    elif r == 165 and g ==94 and b ==60:
        result = [int(250), int(20), int(5)]
    elif r ==74 and g ==114 and b == 52:
        result = [int(randrange(25, 250)), int(randrange(25, 250)), int(randrange(25, 250))]
    else:
        result = [r,g, b]
    return tuple(result)
def apply_filter(img: Image.Image, filt) -> Image.Image:
    for i in range(img.width):
        for j in range(img.height):
            r,g,b = img.getpixel((i, j))
            new_pixel = filt(r,g,b)
            img.putpixel((i, j), new_pixel)
    return img
def process_image(request):
    if request.method == "POST":
        image_file = request.FILES['image']
        image = Image.open(image_file)
        filtered_image = apply_filter(image, GreenFilter)
        filtered_image.save('processed_image.jpg')
        filtered_image.show()
        return HttpResponse('Изображение обработанао и сохранено')
    return render(request, 'upload_image.html')



# def page_not_found(request, exception):
#     return HttpResponseNotFound('<h1>Эта страница не нацдена</h1>')
