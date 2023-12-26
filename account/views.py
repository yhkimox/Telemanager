from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.contrib.auth.forms import UserCreationForm,PasswordResetForm, SetPasswordForm
from django.contrib.auth.forms import UserCreationForm
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
from django.template.loader import render_to_string
from django.http import JsonResponse
from .forms import UserFileForm, UserFileForm2
from .models import UserFile  
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, View
from django.urls import reverse
import os

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
            
    return render(request, 'registration/signup.html',{'form':form})
    
@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account:profile')  # 프로필 페이지로 리다이렉트
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'registration/profile_update.html', {'form': form})

class MyPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('account:profile')
    template_name = 'account/password_change_form.html'

    def form_valid(self, form):
        messages.info(self.request, '암호 변경을 완료했습니다.')
        return super().form_valid(form)
  
class UserPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset.html' #템플릿을 변경하려면 이와같은 형식으로 입력
    success_url = reverse_lazy('account:password_reset_done')
    form_class = PasswordResetForm
    
    def form_valid(self, form):
        if User.objects.filter(email=self.request.POST.get("email")).exists():
            return super().form_valid(form)
        else:
            return render(self.request, 'registration/password_reset_done_fail.html')


    def get(self, request, *args, **kwargs):
        # 암호 변경 폼을 문자열로 렌더링
        form_html = render_to_string(self.template_name, {'form': self.get_form()})
        return JsonResponse({'form_html': form_html}, safe=False)

@login_required
def file_upload(request):
    if request.method == 'POST':
        form = UserFileForm(request.POST, request.FILES)
        if form.is_valid():
            # 현재 로그인한 사용자를 파일에 연결
            user_file = form.save(commit=False)
            user_file.user = request.user
            user_file.save()
            return redirect('client:list') 
    else:
        form = UserFileForm()
    
    files = UserFile.objects.filter(user=request.user)  # 현재 로그인한 사용자의 파일 목록을 가져옵니다.
    return render(request, 'upload/information.html', {'form': form, 'files': files})

# 파일 목록을 출력하는 view입니다.
def file_list(request):
    files = UserFile.objects.filter(user=request.user)
    return render(request, 'upload/list.html', {'files': files})


@login_required
def edit_file(request, file_id):
    file = get_object_or_404(UserFile, id=file_id, user=request.user)
    
    if request.method == 'POST':
        form = UserFileForm2(request.POST, instance=file)
        if form.is_valid():
            form.save()
            return redirect('client:list')  # 클라이언트 목록 뷰로 리디렉션
    else:
        form = UserFileForm2(instance=file)
    
    return render(request, 'upload/edit_file.html', {'form': form, 'file': file})

@login_required
def delete_file(request, file_id):
    file = get_object_or_404(UserFile, id=file_id, user=request.user)
    
    if request.method == 'POST':
        file.delete()
        return redirect('client:list')  # 클라이언트 목록 뷰로 리디렉션
    
    return render(request, 'upload/delete_file.html', {'file': file})


class DeleteSelectedFilesView(LoginRequiredMixin, View):
    def post(self, request):
        selected_ids = request.POST.getlist('file_ids')  
        UserFile.objects.filter(id__in=selected_ids).delete()  
        return redirect(reverse('client:list'))  
