from django.urls import path, reverse, reverse_lazy
from . import views
from .models import *
from django.contrib.auth import views as auth_views
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib import admin
from django.urls import path, include
from .views import *


app_name = 'post'

def generic(request):
    return render(request, '../templates/generic.html')
 
def elements(request):
    return render(request, '../templates/elements.html')


urlpatterns = [

    path('generic.html', generic, name='generic'),
    path('elements.html', elements, name='elements'),
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('list/', views.post_list, name='post_list'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('new/', views.post_new, name='post_new'),
    path('<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('<int:pk>/edit/', views.post_edit, name='post_edit'),
    # path('<int:pk>/comments/', views.comments_create, name='comments_create'),
    # path('<int:pk>/comments/<int:comment_pk>/delete/', views.comments_delete, name='comments_delete'),
    path('<int:pk>/comment/', views.detail, name='detail'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)