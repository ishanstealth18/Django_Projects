from django.http import HttpResponse
from django.shortcuts import render
from .forms import ContactForm

# Create your views here.


def contact(request):

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            return HttpResponse("Form validated successfully!!")
        else:
            return HttpResponse("Bot suspected!!")
    else:
        form = ContactForm()
        return render(request, "contact.html", {'form': form})
