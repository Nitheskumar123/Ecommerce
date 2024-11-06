from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserForm(UserCreationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter User Name'}))
    email=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter User Email'}))
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter User Pass'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter User Pass '}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CustomUserUpdateForm(forms.ModelForm):
    password = None 

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
