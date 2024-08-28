from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render
from expense_tracker_app.forms import login_form, register_form, home_form
from expense_tracker_app.models import ExpenseDataModel


# Create your views here.

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
    page_to_open = None

    if request.method == "POST":
        if form.is_valid():
            user_name = form.cleaned_data["login_username"]
            user_password = form.cleaned_data["login_password"]

            validate_user = authenticate(request, username=user_name, password=user_password)
            if validate_user is not None:
                login(request, validate_user)
        page_to_open = "home.html"

    else:
        page_to_open = "login.html"
        form = login_form.LoginForm

    context = {
        "login_form": form,
    }
    return render(request, page_to_open, context)


def home_page(request):
    form = home_form.HomeForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            category = form.cleaned_data["input_category"]
            amount = form.cleaned_data["input_amount"]
            date = form.cleaned_data["input_date"]
            new_expense_record = ExpenseDataModel(request, expense_category=category, expense_amount=amount,
                                                  expense_date=date)
            new_expense_record.save()
    else:
        form = home_form.HomeForm

    context = {
        'home-form': form,
    }

    return render(request, "home.html", context)

