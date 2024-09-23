from django import forms
from django.forms import TextInput


class RegisterForm(forms.Form):
    register_firstname = forms.CharField(label="First Name", required=True, widget=TextInput(attrs={
        'style': 'width: 300px; margin: 8px 0; border: 1px solid #ccc; border-radius: 4px; '
                 'border-sizing: border-box; padding: 12px 20px;',
    }))
    register_lastname = forms.CharField(label="Last Name", required=True, widget=TextInput(attrs={
        'style': 'width: 300px; margin: 8px 0; border: 1px solid #ccc; border-radius: 4px; '
                 'border-sizing: border-box; padding: 12px 20px;',
    }))
    register_email = forms.CharField(label="Email", required=True, widget=forms.EmailInput(attrs={
        'style': 'width: 300px; margin: 8px 0; border: 1px solid #ccc; border-radius: 4px; '
                 'border-sizing: border-box; padding: 12px 20px;',
    }))
    register_password = forms.CharField(label="Password", required=True, widget=forms.PasswordInput(attrs={
        'style': 'width: 300px; margin: 8px 0; border: 1px solid #ccc; border-radius: 4px; '
                 'border-sizing: border-box; padding: 12px 20px;',
    }))





