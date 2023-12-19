from django.db import models

# Create your models here.


class Client(models.Model):
	name = models.CharField(max_length=70)
	location = models.CharField(max_length=140, null=True, blank=True)
	number = models.CharField(max_length=80, null=True, blank=True)
