from django.contrib import admin
from django.urls import path, include
from accounts.views import task_list, add_task, delete_task, edit_task

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('to-do', task_list, name='task_list'),
    path('to-do/add', add_task, name='add_task'),
    path('to-do/delete/<int:task_id>/', delete_task, name='delete_task'),
    path('to-do/edit/<int:task_id>/', edit_task, name='edit_task'),
    path('', include('accounts.urls')),
]