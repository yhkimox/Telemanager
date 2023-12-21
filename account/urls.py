from django.urls import path, reverse, reverse_lazy
from . import views
from .models import *
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views

app_name = 'account'

urlpatterns = [
    path('', views.page),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/', TemplateView.as_view(template_name='registration/profile.html'), name='profile' ),
    path('profile_update/', views.profile_update, name='profile_update'),
    path('password_change/', views.MyPasswordChangeView.as_view(), name='password_change'),
]
