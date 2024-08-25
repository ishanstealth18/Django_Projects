from django.forms import ModelForm
from e_library_app.models import AddBookModel


class AddBooksForm(ModelForm):
    class Meta:
        model = AddBookModel
        fields = ["title", "summary", "pages", "pdf", "category"]


