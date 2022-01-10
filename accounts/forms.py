from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.fields import ChoiceField


class LoginForm(forms.Form):
    username = forms.CharField( label='Kullanici adi',widget = forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Kullanici Adi'
    }))
    password = forms.CharField( label='Sifre',widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder':'Sifre'
    }))

class RegisterForm(UserCreationForm):    
    is_staff = forms.BooleanField(required=False, label='Ogretmen')
    first_name = forms.CharField( label='Isim',widget = forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Isim'
    }))
    last_name = forms.CharField( label='Soy Isim',widget = forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Soy Isim',
        'label-text':"tex"
    }))
    username = forms.CharField( label='Kullanici adi',widget = forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Kullanici Adi'
    }))
    email = forms.CharField( label='E-mail',widget = forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }))
    password1 = forms.CharField( label='Sifre',widget = forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Sifre'
    }))
    password2 = forms.CharField( label='Sifre Onayi',widget = forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Sifre Onayi'
    }))

    class Meta:
        model = User
        fields = ['is_staff','first_name','last_name','username','email','password1','password2']










# from django import forms

# from .models import Contact

# class ContactForm(forms.ModelForm):
#     first_name = forms.CharField(widget = forms.TextInput(attrs={
#         'class': 'form-control',
#         'placeholder': 'First Name'
#     }))
#     last_name = forms.CharField(widget = forms.TextInput(attrs={
#         'class': 'form-control',
#         'placeholder': 'Last Name'
#     }))
#     email = forms.EmailField(widget = forms.EmailInput(attrs={
#         'class': 'form-control',
#         'placeholder': 'Email'
#     }))
#     phone = forms.CharField(widget = forms.TextInput(attrs={
#         'class': 'form-control',
#         'placeholder': 'Phone'
#     }))
#     message = forms.CharField(widget = forms.Textarea(attrs={
#         'class': 'form-control',
#         'placeholder': 'Message'
#     }))

#     class Meta:
#         model = Contact
#         fields = ['first_name','last_name','email','phone','message']