from django.urls import path, reverse, reverse_lazy
from . import views
from .models import *
from django.shortcuts import render

app_name = 'account'

def login(request):
    return render(request, 'login.html')

urlpatterns = [
    path('login.html', login, name='login'),
]