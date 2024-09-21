from django import forms
from django.forms import TextInput

Category_choices = [("Grocery", "Grocery"), ("House Rent", "House Rent"), ("Restaurant", "Restaurant"), ("Car EMI", "Car EMI"),
                    ("Car And Home Insurance", "Car And Home Insurance"), ("Subscription", "Subscription"), ("Hydro", "Hydro"),
                    ("Furniture", "Furniture"), ("House_Maintenance", "House_Maintenance"),("Mobile And Home Internet", "Mobile And Home Internet"),
                    ("Outing", "Outing"), ("Shopping", "Shopping"), ("Medicines", "Medicines"), ("Car Gas", "Car Gas")]


class HomeForm(forms.Form):
    input_category = forms.CharField(label="Category", required=False, widget=forms.Select(choices=Category_choices, attrs={
        'style': 'width: 300px; margin: 8px 0; border: 1px solid #ccc; border-radius: 4px; '
                 'border-sizing: border-box; padding: 12px 20px;',
    }))

    input_description = forms.CharField(label="Description", required=False,  widget=forms.TextInput(attrs={
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




