from django.urls import path, reverse, reverse_lazy
from . import views
from .models import *
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    path('', views.page),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
]
