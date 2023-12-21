from django.db import models
from django.conf import settings
# Create your models here.


class Client(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=30)                               # 고객 이름 저장
	location = models.CharField(max_length=140, null=True, blank=True)   # 고객 주소 저장
	number = models.CharField(max_length=20, null=True, blank=True)      # 고객 전화번호 저장
	birth_date = models.CharField(max_length=10, null=True, blank=True)  # YYYY-MM_DD 형식 
	tm_date = models.DateTimeField(null=True, blank = True)              # TM 날짜 저장
	age = models.IntegerField(null= True, blank=True)                    # 고객 나이 저장
	gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], null=True, blank=True)  # (실제 값, 보여지는 값)
	email = models.EmailField(max_length=254, null=True, blank=True)     # 고객 이메일 저장
 
 
