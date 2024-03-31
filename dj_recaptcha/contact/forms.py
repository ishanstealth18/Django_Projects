from django import forms
from captcha.fields import CaptchaField


class ContactForm(forms.Form):
    email = forms.EmailField()
    feedback = forms.CharField(widget=forms.Textarea)
    captcha = CaptchaField()
