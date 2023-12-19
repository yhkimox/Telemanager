from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static

def index(request):
    return render(request, 'home.html')

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', index),
    path('account/', include('account.urls')),
    path('chatbot/', include('chatbot.urls')),
    path('client/', include('client.urls')),
]