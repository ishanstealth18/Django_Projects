from django import forms
from django.forms import TextInput

CATEGORY_CHOICES = ['Grocery', 'Dollarama', 'Restaurants', 'Costco', 'House Rent', 'Internet and Mobile', 'Car', 'House'
                    'and Car Insurance']


class HomeForm(forms.Form):
    input_category = forms.CharField(label="Category", required=False, widget=forms.Select(choices=CATEGORY_CHOICES, attrs={
        'style': 'width: 300px; margin: 8px 0; border: 1px solid #ccc; border-radius: 4px; '
                 'border-sizing: border-box; padding: 12px 20px;',
    }))

    input_amount = forms.IntegerField(label="Amount", required=False, widget=forms.TextInput(attrs={
        'style': 'width: 300px; margin: 8px 0; border: 1px solid #ccc; border-radius: 4px; '
                 'border-sizing: border-box; padding: 12px 20px;',
    }))

    input_date = forms.CharField(label="Date", required=False, widget=forms.DateTimeInput(attrs={
        'style': 'width: 300px; margin: 8px 0; border: 1px solid #ccc; border-radius: 4px; '
                 'border-sizing: border-box; padding: 12px 20px;',
    }))

