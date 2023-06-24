from django import forms 
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User 

class CustomerLoginForm(UserCreationForm):
    password1=forms.CharField(label="Enter the Password",widget=forms.PasswordInput(attrs={"class":"form-control"}))
    
    password2=forms.CharField(label="Enter the Password again",widget=forms.PasswordInput(attrs={"class":"form-control"}))
    
    email=forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control"}))
    
    class Meta:
        model=User 
        fields=["username","email","password1","password2"]
        label={"email":"Enter the email"}
        widgets={"username":forms.TextInput(attrs={"class":"form-control"})}