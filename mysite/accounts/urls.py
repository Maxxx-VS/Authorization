from django.urls import path, include, register_converter
from . import views
from . import converters

register_converter(converters.FourDigitYearConverter, 'year4')

urlpatterns = [
    path('', views.index, name='home'),
    path('news', views.news, name='news'),
    path('about', views.about, name='about'),
    path('contacts', views.contacts, name='contacts'),
    path('blog/', views.blog, name='blog'),
    path('cooking/', views.cooking, name='cooking'),
    path('plov', views.plov),
    path('soup', views.soup),
    path('porridge', views.porridge),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('post/<int:post_id>/', views.show_post, name='post'),
]
