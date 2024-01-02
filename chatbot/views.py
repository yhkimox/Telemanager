from django.shortcuts import render
from django.urls import reverse

# Create your views here.
def chat(request):
    return render(request, 'chatbot/chat.html')

def test(request):
    return render(request, 'chatbot/test.html')
