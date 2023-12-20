from django.db import models

# Create your models here.


class Client(models.Model):
	name = models.CharField(max_length=30)
	location = models.CharField(max_length=140, null=True, blank=True)
	number = models.CharField(max_length=20, null=True, blank=True)
	birth_date = models.CharField(max_length=10, null=True, blank=True)  # YYYY-MM_DD 형식 
	age = models.IntegerField(null= True, blank=True)
	gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], null=True, blank=True)  # (실제 값, 보여지는 값)
 
	
