from django.urls import path, reverse, reverse_lazy
from . import views
from .models import *
from django.contrib.auth import views as auth_views

from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static

app_name = 'account'

def index(request):
    return render(request, '../templates/index.html')

def generic(request):
    return render(request, '../templates/generic.html')
 
def elements(request):
    return render(request, '../templates/elements.html')


urlpatterns = [
    path('index.', views.index, name='index'),
    
    path('index.html', index, name='index'),
    path('generic.html', generic, name='generic'),
    path('elements.html', elements, name='elements'),
    
    path('', views.index),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)