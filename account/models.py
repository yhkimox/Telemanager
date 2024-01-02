from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# default=True 제거: 기본값을 설정하지 않습니다.
# null=True 추가: 이 필드는 null 값을 허용합니다.
# blank=True 추가: 이 필드는 폼에서 필수가 아닙니다.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username  # 사용자의 이름을 반환합니다.
    
class CompanyFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='company_data_files/')
    embedding_file = models.FileField(upload_to='embedding_files/', blank=True, null=True)


    def __str__(self):
        return self.file.name