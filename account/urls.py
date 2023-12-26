from django.urls import path, reverse, reverse_lazy
from . import views
from .models import *
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

app_name = 'account'

def generic(request):
    return render(request, '../templates/generic.html')
 
def elements(request):
    return render(request, '../templates/elements.html')


urlpatterns = [
    path('generic.html', generic, name='generic'),
    path('elements.html', elements, name='elements'),
    path('', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/', TemplateView.as_view(template_name='registration/profile.html'), name='profile' ),
    path('profile_update/', views.profile_update, name='profile_update'),
    path('password_change/', views.MyPasswordChangeView.as_view(), name='password_change'),
    path('password_reset/', views.UserPasswordResetView.as_view(), name="password_reset"),
    path('password_reset_done/', views.UserPasswordResetDoneView.as_view(), name="password_reset_done"),
    # path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('password_reset_complete/', views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)