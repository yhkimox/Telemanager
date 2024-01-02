from django.shortcuts import render
from django.urls import reverse

# Create your views here.
def chat(request):
    return render(request, 'chatbot/chat.html')

def index(request):
    # app_name: URL 패턴을 정의할 때 설정한 app_name
    # 'client:index': app_name과 패턴 이름을 조합한 것
    url = reverse('chatbot:index') # 
    return render(request, 'index.html', {'index_url': url})