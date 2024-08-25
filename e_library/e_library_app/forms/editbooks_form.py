from django.forms import ModelForm
from e_library_app.models import AddBookModel
from django import forms


class EditBooksForm(ModelForm):

    # Adding extra field to display
    current_pdf = forms.CharField()

    class Meta:
        model = AddBookModel
        fields = ["title", "summary", "pages", "current_pdf", "pdf", "category"]

