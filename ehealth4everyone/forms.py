from django import forms
from django.forms import ModelForm, PasswordInput
from .models import Profile, User



class SignupForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','password']
        widgets = {
            'password' : PasswordInput(),
        }

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ('user','disease',)