from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import logout
# Create your views here.

def index(request):
    return render(request, 'post/index.html')
