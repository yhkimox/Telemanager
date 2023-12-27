from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.contrib.auth.forms import UserCreationForm,PasswordResetForm
from django.conf import settings
from .forms import SignupForm
from django.contrib.auth.views import PasswordChangeView,PasswordResetView, PasswordResetDoneView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.http import JsonResponse
from .forms import CompanyFileForm, CompanyFileForm2
from .models import CompanyFile 

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, View
from django.urls import reverse
import os
from django.core.files.storage import FileSystemStorage
from django.contrib import messages

from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders.csv_loader import CSVLoader

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

# 비밀번호 찾기
class UserPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset.html' #템플릿을 변경하려면 이와같은 형식으로 입력
    success_url = reverse_lazy('account:password_reset_done')
    form_class = PasswordResetForm
    
    def form_valid(self, form):
        email = self.request.POST.get("email")
        if User.objects.filter(email=email).exists():
            return super().form_valid(form)
        else:
            return JsonResponse({'email_not_exists': True})
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        # 존재하지 않는 이메일인 경우에 대한 처리
        return JsonResponse({'email_not_exists': True})

@login_required
def file_upload(request):
    if request.method == 'POST':
        form = CompanyFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']  # 업로드된 파일을 가져옵니다.
            fs = FileSystemStorage(location='media/company_data_files/')
            
            # 파일의 이름이 이미 존재하는지 확인합니다.
            if not fs.exists(uploaded_file.name):
                user_file = form.save(commit=False)
                user_file.user = request.user
                user_file.file = uploaded_file  # 파일 객체를 모델 필드에 할당합니다.
                
                # loader = CSVLoader(file_path='/content/drive/MyDrive/langchain/card.csv', source_column='카드명')
                loader = CSVLoader(file_path='/content/drive/MyDrive/langchain/card.csv')
                data = loader.load()
                
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                texts = text_splitter.split_documents(data)
                ##################################################
                # hugging face 임베딩 저장
                model_name = "jhgan/ko-sroberta-multitask"
                model_kwargs = {'device': 'cpu'}
                encode_kwargs = {'normalize_embeddings': False}

                hf = HuggingFaceEmbeddings(
                    model_name=model_name,
                    model_kwargs=model_kwargs,
                    encode_kwargs=encode_kwargs
                )
                
                ###################################################
                # embedding vector 저장
                vectordb_hf = Chroma.from_documents(
                    documents=texts,
                    embedding=hf, persist_directory="/chroma_db_hf")
                vectordb_hf.persist()
                ##################################################
                
                
                user_file.save()
                return redirect('client:list')
            else:
                # 이미 존재하는 파일 이름이면 여기로 이동
                messages.warning(request, '동일한 파일 이름이 이미 존재합니다.')
                return redirect('client:list')  
    else:
        form = CompanyFileForm()
    
    files = CompanyFile.objects.filter(user=request.user)
    return render(request, 'upload/information.html', {'form': form, 'files': files})

# 파일 목록을 출력하는 view입니다.
def file_list(request):
    files = CompanyFile.objects.filter(user=request.user)
    return render(request, 'upload/list.html', {'files': files})


@login_required
def edit_file(request, file_id):
    file = get_object_or_404(CompanyFile, id=file_id, user=request.user)
    
    if request.method == 'POST':
        form = CompanyFileForm2(request.POST, instance=file)
        if form.is_valid():
            form.save()
            return redirect('client:list')  # 클라이언트 목록 뷰로 리디렉션
    else:
        form = CompanyFileForm2(instance=file)
    
    return render(request, 'upload/edit_file.html', {'form': form, 'file': file})

@login_required
def delete_file(request, file_id):
    file = get_object_or_404(CompanyFile, id=file_id, user=request.user)
    
    if request.method == 'POST':
        file.delete()
        return redirect('client:list')  # 클라이언트 목록 뷰로 리디렉션
    
    return render(request, 'upload/delete_file.html', {'file': file})


class DeleteSelectedFilesView(LoginRequiredMixin, View):
    def post(self, request):
        selected_ids = request.POST.getlist('file_ids')  
        CompanyFile.objects.filter(id__in=selected_ids).delete()  
        return redirect(reverse('client:list'))  

