from django import forms


class ViewExpenseForm(forms.Form):
    expense_from_date = forms.DateTimeField(label="From Date", required=True, widget=forms.DateInput(attrs={
        'type': 'date',
        'style': 'width: 300px; margin: 8px 0; border: 1px solid #ccc; border-radius: 4px; '
                 'border-sizing: border-box; padding: 12px 20px;',
    }))
    expense_to_date = forms.DateTimeField(label="To Date", required=True, widget=forms.DateInput(attrs={
        'type': 'date',
        'style': 'width: 300px; margin: 8px 0; border: 1px solid #ccc; border-radius: 4px; '
                 'border-sizing: border-box; padding: 12px 20px;',
    }))


