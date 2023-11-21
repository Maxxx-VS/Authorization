from django.urls import path, include, register_converter
from . import views
from . import converters
from . views import process_image

register_converter(converters.FourDigitYearConverter, 'year4')

urlpatterns = [
    path('', views.index, name='home'),
    path('news', views.news, name='news'),
    path('about', views.about, name='about'),
    path('contacts', views.contacts, name='contacts'),
    path('blog/', views.blog, name='blog'),
    path('cooking/', views.cooking, name='cooking'),
    path('plov/<int:portion>/', views.plov),
    path('soup/<int:portion>/', views.soup),
    path('porridge/<int:portion>/', views.porridge),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('post/<int:post_id>/', views.show_post, name='post'),
    path('process_image/', process_image, name='process_image'),
]

