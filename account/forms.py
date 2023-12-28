from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm as AuthPasswordChangeForm
from django import forms
from .models import Profile
from django.contrib.auth.models import User
from .models import CompanyFile

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

        

class CompanyFileForm(forms.ModelForm):
    class Meta:
        model = CompanyFile
        fields = ['description', 'file']
        
class CompanyFileForm2(forms.ModelForm):  # 삭제할 때 사용
    class Meta:
        model = CompanyFile
        fields = ['description']

class PasswordChangeForm(AuthPasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Present Password"},
        )
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Change Password"})
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Change Password Confirm"})
    )

    def clean(self):
        old_password = self.cleaned_data.get("old_password")
        new_password1 = self.cleaned_data.get("new_password1")

        if old_password == new_password1:
            self.add_error(
                "old_password",
                forms.ValidationError("it is same old password with new one"),
            )
        else:
            return self.cleaned_data