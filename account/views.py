from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from .forms import SignupForm
from django.http import HttpResponse
from django.contrib.auth import logout
# Create your views here.

def index(request):
    return render(request, 'registration/login.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(settings.LOGIN_URL)
    else:
        form = SignupForm()
            
    return render(request, 'registration/login.html', {'form':form})


def logout(request):
    logout(request)
    return redirect('index')  # 로그아웃 후 리다이렉션할 페이지의 이름 또는 경로