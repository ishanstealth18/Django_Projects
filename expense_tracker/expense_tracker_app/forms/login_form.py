from django import forms
from django.forms import TextInput, PasswordInput


class LoginForm(forms.Form):
    login_username = forms.CharField(label="Username", required=True, widget=TextInput(attrs={
        'style': 'width: 300px; margin: 8px 0; display: inline-block; border: 1px solid #ccc; border-radius: 4px; '
                 'border-sizing: border-box; padding: 12px 20px;',
        'class': 'form-control',
    }))
    login_password = forms.CharField(label="Password", required=True, widget=PasswordInput(attrs={
        'style': 'width: 300px; margin: 8px 0; display: inline-block; border: 1px solid #ccc; border-radius: 4px; '
                 'border-sizing: border-box; padding: 12px 20px; ',
        'class': 'form-control',
    }))
