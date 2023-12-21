from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'location', 'number']  


"""
from django import forms

class FileUploadForm(forms.Form):
    excel_file = forms.FileField(label='파일 업로드', help_text='Excel 또는 CSV 파일 지원 (.xlsx, .xls, .csv)')
"""