from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest
from django.views.generic import ListView
import pandas as pd
from .models import Client
from .forms import ClientForm  # 고객 모델 폼
from django.urls import reverse

class ClientListView(ListView):
    model = Client
    template_name = 'client/client_list.html'  
    context_object_name = 'client_list'  # 템플릿에서 사용할 컨텍스트 변수 이름
    paginate_by = 5  # 한 페이지에 표시할 객체 수
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # 컨텍스트 데이터 가져옴

       
        context['tmgoal'] = self.request.session.get('tmgoal', None)

        return context
    
    
def upload_excel(request):
    if request.method == 'POST':
        excel_file = request.FILES['excel_file']
        tmgoal = request.POST.get('tmgoal')
        request.session['tmgoal'] = tmgoal
        df = pd.read_excel(excel_file)
        print(df.columns)

        for index, row in df.iterrows():
            Client.objects.create(
                name = row['name'], 
                location = row['location'],
                number = row['number'],
            )
            
        
        return redirect('client:list')
    
    return render(request, 'client/upload.html')

def edit_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client:list')  # 클라이언트 목록 뷰로 리디렉션
    else:
        form = ClientForm(instance=client)
    
    return render(request, 'client/edit_client.html', {'form': form, 'client': client})

def delete_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    
    if request.method == 'POST':
        client.delete()
        return redirect('client:list')  # 클라이언트 목록 뷰로 리디렉션
    
    return render(request, 'client/delete_client.html', {'client': client})


### 원하는 정보 찾는 view - test용
def test(request):
    
    client_list = Client.objects.filter(name__icontains='민')
    
    return render(request,'client/test.html',{'client_list': client_list})

