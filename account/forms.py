from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import Profile
from django.contrib.auth.models import User
from .models import UserFile

class SignupForm(UserCreationForm):
    
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', )
        
    def save(self):
        user = super().save()
        Profile.objects.create(user=user,)
        
        return user
    
class ProfileUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()
<<<<<<< HEAD
        self.fields['password'].required = False
=======
        self.fields['password'].required = False
        

class UserFileForm(forms.ModelForm):
    class Meta:
        model = UserFile
        fields = ['description', 'file']
        
class UserFileForm2(forms.ModelForm):  # 삭제할 때 사용
    class Meta:
        model = UserFile
        fields = ['description']
>>>>>>> c88672412f5de324b90ee047e4c27b88a117b68a
