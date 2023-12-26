from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import Profile
from django.contrib.auth.models import User

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
        self.fields['password'].required = False