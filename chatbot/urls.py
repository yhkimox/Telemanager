from django.urls import path, reverse, reverse_lazy
from . import views
from .models import *
from django.shortcuts import render

app_name = 'chatbot'

def chat(request):
    return render(request, 'chat.html')

urlpatterns = [
    path('chat.html', chat, name='chat'),
]
