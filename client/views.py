from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest
from django.views.generic import ListView, View
import pandas as pd
from .models import Client, Marketing
from .forms import ClientForm  # 고객 모델 폼
from django.urls import reverse
from datetime import datetime
import os
import zipfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import logging # 디버그 로그 확인


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'client/client_list.html'  
    context_object_name = 'client_list'  # 템플릿에서 사용할 컨텍스트 변수 이름
    paginate_by = 10  # 한 페이지에 표시할 객체 수
    
    def get_context_data(self, **kwargs): # 2
        context = super().get_context_data(**kwargs)  # 컨텍스트 데이터 가져옴
        context['tmgoal'] = self.request.session.get('tmgoal', None)

        return context

    def post(self, request, *args, **kwargs):
        selected_ids = request.POST.getlist('client_ids')  
        Client.objects.filter(id__in=selected_ids).delete()  
        return redirect(reverse('client:list'))  
    
    def get_queryset(self): # 1 엑셀 데이터는 계속 저장되어 왔는데 이게 출력이 안되는 것일 뿐...
        user = self.request.user
        #print(f"Current User ID: {user.id}")
        queryset = Client.objects.filter(user=self.request.user).order_by('-tm_date')  # '-tm_date'는 내림차순 정렬을 의미
        #print(f"Queryset length: {queryset.count()}")
        #print(f"Queryset data: {queryset.values()}")
        return queryset


# 수정사항 - 마케팅 정보 저장
class MarketingListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'client/client_list.html'  
    context_object_name = 'file_list'  # 템플릿에서 사용할 컨텍스트 변수 이름
    paginate_by = 10  # 한 페이지에 표시할 객체 수
    
    def get_context_data(self, **kwargs): # 2
        context = super().get_context_data(**kwargs)  # 컨텍스트 데이터 가져옴
        context['tmgoal'] = self.request.session.get('tmgoal', None)

        return context

    def post(self, request, *args, **kwargs):
        selected_ids = request.POST.getlist('file_ids')  
        Client.objects.filter(id__in=selected_ids).delete()  
        return redirect(reverse('client:list'))  
    
    def get_queryset(self): # 1 엑셀 데이터는 계속 저장되어 왔는데 이게 출력이 안되는 것일 뿐...
        user = self.request.user
        #print(f"Current User ID: {user.id}")
        queryset = Client.objects.filter(user=self.request.user).order_by('-tm_date')  # '-tm_date'는 내림차순 정렬을 의미
        #print(f"Queryset length: {queryset.count()}")
        #print(f"Queryset data: {queryset.values()}")
        return queryset


class DeleteSelectedClientsView(View):
    def post(self, request):
        selected_ids = request.POST.getlist('client_ids')  
        Client.objects.filter(id__in=selected_ids).delete()  
        return redirect(reverse('client:list'))  


def normalize_gender(gender_str):
    # 성별을 Male, Female로 변환
    
    if gender_str in ['남성', '남', '남자', 'm', 'M']:
        return 'Male'
    elif gender_str in ['여성', '여', '여자', 'f', 'F']:
        return 'Female'
    else:
        return None  
    

    
def upload_excel(request): # 이상 없음.
    if request.method == 'POST':
        excel_file = request.FILES['excel_file']
        tmgoal = request.POST.get('tmgoal')
        request.session['tmgoal'] = tmgoal
        df = pd.read_excel(excel_file)
        
        # birth_date 같은 경우 문자열로 변환
        df['birth_date'] = df['birth_date'].astype(str)
        
        print(df.columns)

        for index, row in df.iterrows():
            name = str(row['name'])
            number = row['number']
            email = row['email']
            print(email)
            
            # 기존에 손님 데이터와 중복되는 데이터인지 확인
            existing_client = Client.objects.filter(name=name, number=number, email=email).first()
            if existing_client:
                continue
            
            # raw_birth_date 에는 마스킹 전 생년월일
            raw_birth_date = row.get('birth_date', None)
            
            # 생년월일이 엑셀로 들어올 경우, age 계산
            if raw_birth_date:
                birth_date = datetime.strptime(raw_birth_date, '%Y-%m-%d')
                today = datetime.today()
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            
            # 생년월일이 없을 경우,     
            else:  
                age = None
            
            # 생년월일 마스킹        
            masked_birth_date = raw_birth_date[:5] + 'XX-XX'
            
            
            # 정규화 전 성별
            raw_gender = row.get('gender', None)
            
            # 성별 변환
            normalized_gender = normalize_gender(raw_gender)
            
            temp_date = datetime.now()
            
            user = request.user # 문제는 원래 저장되어 있던 데이터여서 새로 안된거일 뿐이었다. 데이터베이스를 초기화하는 코드가 약간 필요할듯 하다.
            #if user.is_authenticated:
            #    print(f"User ID: {user.pk}")
            #else:
            #    print("User is not authenticated.")
            Client.objects.create(
                user = user,
                name = name,
                location = row['location'],
                number = number,
                birth_date = masked_birth_date,
                age = age,
                tm_date = temp_date,
                gender = normalized_gender,
                email = email,
            )
        print(f"Client {Client.id} created successfully.")  # 디버깅 메시지 잘뜬다.
        return redirect('client:list')
    
    
    return render(request, 'client/upload.html')


def edit_client(request, client_id):
    client = get_object_or_404(Client, id=client_id, user=request.user)
    
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client:list')  # 클라이언트 목록 뷰로 리디렉션
    else:
        form = ClientForm(instance=client)
    
    return render(request, 'client/edit_client.html', {'form': form, 'client': client})

@login_required
def delete_client(request, client_id):
    client = get_object_or_404(Client, id=client_id, user=request.user)
    
    if request.method == 'POST':
        client.delete()
        return redirect('client:list')  # 클라이언트 목록 뷰로 리디렉션
    
    return render(request, 'client/delete_client.html', {'client': client})


### 원하는 정보 찾는 view - test용
def test(request):
    
    client_list = Client.objects.filter(name__icontains='민')
    
    return render(request,'client/test.html', {'client_list': client_list})


def open_modal(request):
    return render(request, 'client/modal_content.html')