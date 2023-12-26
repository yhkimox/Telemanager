from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth.forms import UserCreationForm,PasswordResetForm, SetPasswordForm
from django.conf import settings
from .forms import SignupForm
from django.contrib.auth.views import PasswordChangeView,PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


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
            
    return render(request, 'registration/login.html',{'form':form})
    

def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account:profile')  # 프로필 페이지로 리다이렉트
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'profile_update.html', {'form': form})

class MyPasswordChangeView(PasswordChangeView):
    success_url=reverse_lazy('account:profile')
    template_name='account/password_change_form.html'
    
    def form_valid(self, form):
        messages.info(self.request, '암호 변경을 완료했습니다.')
        return super().form_valid(form)
    
# class UserPasswordResetView(PasswordResetView):
#     template_name = 'registration/password_reset.html' #템플릿을 변경하려면 이와같은 형식으로 입력
#     success_url = reverse_lazy('account:password_reset_done')
#     form_class = PasswordResetForm
    
#     def form_valid(self, form):
#         if User.objects.filter(email=self.request.POST.get("email")).exists():
#             return super().form_valid(form)
#         else:
#             return render(self.request, 'registration/password_reset_done_fail.html')
            
# class UserPasswordResetDoneView(PasswordResetDoneView):
#     template_name = 'registration/password_reset_done.html'
UserModel = get_user_model()
INTERNAL_RESET_URL_TOKEN = 'set-password'
INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'

class UserPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset.html' #템플릿을 변경하려면 이와같은 형식으로 입력
    success_url = reverse_lazy('account:password_reset_done')
    form_class = PasswordResetForm
    
    def form_valid(self, form):
        if User.objects.filter(email=self.request.POST.get("email")).exists():
            return super().form_valid(form)
        else:
            return render(self.request, 'registration/password_reset_done_fail.html')
            
class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html' #템플릿을 변경하려면 이와같은 형식으로 입력

class UserPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = SetPasswordForm
    success_url=reverse_lazy('password_reset_complete')
    template_name = 'registration/password_reset_confirm.html'

    def form_valid(self, form):
        return super().form_valid(form)

class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = resolve_url(settings.LOGIN_URL)
        return context