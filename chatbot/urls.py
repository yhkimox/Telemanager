from django.urls import path, reverse, reverse_lazy
from . import views
from .models import *
from django.shortcuts import render


app_name = 'chatbot'

def chat(request):
    return render(request, 'chat.html')



urlpatterns = [
    path('', views.chat, name='chat'),
    path('index/', views.index, name='index'),
    #path('edit/<int:client_id>/', views.edit_client, name='edit_client'),
]

