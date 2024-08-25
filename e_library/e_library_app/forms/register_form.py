from django import forms
from django.forms import ModelForm
from e_library_app.models import RegisterModel


class RegisterForm(ModelForm):
    class Meta:
        model = RegisterModel
        fields = ["first_name", "last_name", "email_address", "password"]