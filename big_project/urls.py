# big_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static

def index(request):
    return render(request, 'index.html')

def generic(request):
    return render(request, 'generic.html')

def elements(request):
    return render(request, 'elements.html')

urlpatterns = [
    path('', index),
    path("admin/", admin.site.urls),
    path('account/', include('account.urls')),
    path('chatbot/', include('chatbot.urls')),
    path('client/', include('client.urls')),
    path('index.html', index, name='index'),  # /index.html에 대한 URL 패턴 추가
    path('generic.html', generic, name='generic'), 
    path('elements.html', elements, name='elements'), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
