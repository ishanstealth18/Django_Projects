from django import forms
from django.forms import TextInput


class RegisterForm(forms.Form):
    register_firstname = forms.CharField(label="First Name", required=False, widget=TextInput(attrs={
        'style': 'width: 300px; margin: 8px 0; display: inline-block; border: 1px solid #ccc; border-radius: 4px; '
                 'border-sizing: border-box; padding: 12px 20px;',
        'class': 'form-control',
    }))
    register_lastname = forms.CharField(label="Last Name", required=False, widget=TextInput(attrs={
        'style': 'width: 300px; margin: 8px 0; display: inline-block; border: 1px solid #ccc; border-radius: 4px; '
                 'border-sizing: border-box; padding: 12px 20px;',
        'class': 'form-control',
    }))
    register_email = forms.CharField(label="Email", required=False, widget=forms.EmailInput(attrs={
        'style': 'width: 300px; margin: 8px 0; display: inline-block; border: 1px solid #ccc; border-radius: 4px; '
                 'border-sizing: border-box; padding: 12px 20px;',
        'class': 'form-control',
    }))
    register_password = forms.CharField(label="Password", required=False, widget=forms.PasswordInput(attrs={
        'style': 'width: 300px; margin: 8px 0; display: inline-block; border: 1px solid #ccc; border-radius: 4px; '
                 'border-sizing: border-box; padding: 12px 20px;',
        'class': 'form-control',
    }))





