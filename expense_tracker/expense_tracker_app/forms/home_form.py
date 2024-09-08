from django import forms
from django.forms import TextInput

Category_choices = [("Grocery", "Grocery"), ("House_Rent", "House_Rent"), ("Restaurant", "Restaurant"), ("Car_EMI", "Car_EMI"),
                    ("Car_Insurance", "Car_Insurance"), ("Home_Insurance", "Home_Insurance"), ("Hydro", "Hydro"),
                    ("Entertainment", "Entertainment"), ("Subscription", "Subscription"), ("House_Maintenance", "House_Maintenance"),
                    ("Outing", "Outing"), ("Shopping", "Shopping"), ("Car", "Car")]


class HomeForm(forms.Form):
    input_category = forms.CharField(label="Category", required=False, widget=forms.Select(choices=Category_choices, attrs={
        'style': 'width: 300px; margin: 8px 0; border: 1px solid #ccc; border-radius: 4px; '
                 'border-sizing: border-box; padding: 12px 20px;',
    }))

    input_amount = forms.DecimalField(label="Amount", required=False, widget=forms.TextInput(attrs={
        'style': 'width: 300px; margin: 8px 0; border: 1px solid #ccc; border-radius: 4px; '
                 'border-sizing: border-box; padding: 12px 20px;',
    }))

    input_date = forms.DateField(label="Date", required=False, widget=forms.DateInput(attrs={
        'type': 'date',
        'style': 'width: 300px; margin: 8px 0; border: 1px solid #ccc; border-radius: 4px; '
                 'border-sizing: border-box; padding: 12px 20px;',
    }))


