from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import ProfileModel, AttendanceModel

class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class LoginForm(AuthenticationForm):
    pass



class ProfileForm(forms.ModelForm):
    class Meta:
        model = ProfileModel
        fields = ['department', 'designation', 'salary', 'photo']



class CustomPasswordChangeForm(PasswordChangeForm):
    pass




class AttendanceForm(forms.ModelForm):
    class Meta:
        model = AttendanceModel
        fields = ['employee', 'date', 'check_in_time', 'check_out_time', 'status']
        
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'check_in_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'check_out_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
        }