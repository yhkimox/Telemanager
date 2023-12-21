from django.urls import path, reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from . import views
from .models import *
from .views import ClientListView
from django.shortcuts import render


app_name = 'client'

def index(request):
    return render(request, 'index.html')

urlpatterns = [
    path('list/', ClientListView.as_view(), name = 'list'),
    path('test/', views.test, name='test'),
    path('upload/', views.upload_excel, name='upload'),
    path('upload2/', views.upload_excel2, name='upload2'),
    path('edit/<int:client_id>/', views.edit_client, name='edit_client'),
    path('delete/<int:client_id>/', views.delete_client, name='delete_client'),
    path('index.html', index, name='index'),

    path('delete_selected/', views.DeleteSelectedClientsView.as_view(), name='delete_selected')
]


