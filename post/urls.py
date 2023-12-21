from django.urls import path, reverse, reverse_lazy
from . import views
from .models import *
from django.contrib.auth import views as auth_views

from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include

app_name = 'post'

def generic(request):
    return render(request, '../templates/generic.html')
 
def elements(request):
    return render(request, '../templates/elements.html')


urlpatterns = [

    path('generic.html', generic, name='generic'),
    path('elements.html', elements, name='elements'),
    
    path('', views.index, name="index"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)