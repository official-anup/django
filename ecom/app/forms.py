
from django import forms 
from django.contrib.auth.forms import UserCreationForm ,AuthenticationForm,UsernameField,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext,gettext_lazy as _
from django.contrib.auth import password_validation

from app.models import Customer

class CustomerRegiForm(UserCreationForm):
    password1=forms.CharField(label="Enter the Password",widget=forms.PasswordInput(attrs={"class":"form-control"}))
    
    password2=forms.CharField(label="Enter the Password again",widget=forms.PasswordInput(attrs={"class":"form-control"}))
    
    email=forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control"}))
    
    class Meta:
        model=User 
        fields=["username","email","password1","password2"]
        label={"email":"Enter the email"}
        widgets={"username":forms.TextInput(attrs={"class":"form-control"})}
        
    
class LoginForm(AuthenticationForm):
        username=UsernameField(widget=forms.TextInput(attrs={'autofocus':True,"class":"form-control"}))
        
        password=forms.CharField(label=_("Password"),strip=False,widget=forms.TextInput(attrs={'autocomplete':True,"class":"form-control"}))

class ChangePassword(PasswordChangeForm):
    old_password=forms.CharField(label=_("Old Password"),strip=False,widget=forms.PasswordInput(attrs={"autocomplete":"current-password","autofocus":True,"class":"form-control"}))
    
    new_password1=forms.CharField(label=_("new Password"),strip=False,widget=forms.PasswordInput(attrs={"autocomplete":"new-password","class":"form-control"}),help_text=password_validation.password_validators_help_text_html())
    
    new_password2=forms.CharField(label=_("Confirm new Password"),strip=False,widget=forms.PasswordInput(attrs={"autocomplete":"new-password","class":"form-control"}))
    
class MyPasswordResetForm(PasswordResetForm):
    email=forms.EmailField(label=_(" Email "),max_length=250,widget=forms.EmailInput(attrs={"autocomplete":"emial","class":"form-control"}))

class MyPasswordResetConfirm(SetPasswordForm):
    new_password1=forms.CharField(label=_("New Password"),strip=False,widget=forms.PasswordInput(attrs={"autocomplete":"new-password","class":"form-control"}),help_text=password_validation.password_validators_help_text_html())
    
    new_password1=forms.CharField(label=_("Confirm new Password"),strip=False,widget=forms.PasswordInput(attrs={"autocomplete":"new-password","class":"form-control"}))

    
class CustomerProfileForms(forms.ModelForm):
    class Meta:
        model=Customer
        fields=["name","locality","city","state","zipcode"]
        widgets={"name":forms.TextInput(attrs={"class":"form-control"}),
                 
        "locality":forms.TextInput(attrs={"class":"form-control"}),
        
        "city":forms.TextInput(attrs={"class":"form-control"}),
        
        "state":forms.Select(attrs={"class":"form-control"}),
        
        "zipcode":forms.NumberInput(attrs={"class":"form-control"})
        
        }
        
