from django.urls import path, reverse, reverse_lazy
from . import views
from .models import *

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
    path('', views.index, name='index'),
    path('signup.html', views.signup, name='signup'),
    path('index.html', index, name='index'),
    path('generic.html', generic, name='generic'),
    path('elements.html', elements, name='elements'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)