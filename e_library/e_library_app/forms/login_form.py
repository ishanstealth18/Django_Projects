from django import forms


class LoginForm(forms.Form):
    login_email_address = forms.CharField(label="Email Address", max_length=100)
    login_password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)
