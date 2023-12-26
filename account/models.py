from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class UserFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='user_files/')

    def __str__(self):
        return self.file.name