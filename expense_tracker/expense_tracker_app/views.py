from django.contrib.auth import authenticate
from django.contrib.auth.models import User
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
    if request.method == "POST":
        if form.is_valid():
            first_name = form.cleaned_data["register_firstname"]
            last_name = form.cleaned_data["register_lastname"]
            email = form.cleaned_data["register_email"]
            password = form.cleaned_data["register_password"]
            new_user_record = User.objects.create_user(first_name=first_name, last_name=last_name, email=email,
                                                       password=password, username=first_name)
            new_user_record.save()

    form = register_form.RegisterForm
    context = {
        "register_form": form,
    }
    return render(request, "register.html", context)


def user_login(request):
    form = login_form.LoginForm(request.POST)

    if request.method == "POST":
        if form.is_valid():
            user_name = form.cleaned_data["login_username"]
            user_password = form.cleaned_data["login_password"]

            validate_user = authenticate(request, username=user_name, password=user_password)
            if validate_user is not None:
                login(request)
    else:
        form = login_form.LoginForm

    context = {
        "login_form": form,
    }
    return render(request, "login.html", context)

