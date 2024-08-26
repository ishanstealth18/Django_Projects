from django.shortcuts import render
from expense_tracker_app.forms import login_form, register_form


# Create your views here.

def login(request):
    form = login_form.LoginForm(request.POST)

    context = {
        "login_form": form,
    }
    return render(request, "login.html", context)


def register_user(request):
    form = register_form.RegisterForm(request.POST)

    context = {
        "register_form": form,
    }
    return render(request, "register.html", context)
