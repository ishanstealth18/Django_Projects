from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from expense_tracker_app.forms import login_form, register_form, home_form, view_expense_form
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

    if request.method == "POST":
        if form.is_valid():
            user_name = form.cleaned_data["login_username"]
            user_password = form.cleaned_data["login_password"]

            validate_user = authenticate(request, username=user_name, password=user_password)
            if validate_user is not None:
                login(request, validate_user)
        return redirect("home.html")

    else:
        page_to_open = "login.html"
        form = login_form.LoginForm

        context = {
            "login_form": form,
        }
        return render(request, page_to_open, context)


def home_page(request):
    form = home_form.HomeForm(request.POST)
    user = User.objects.all().get(id=request.user.id)
    if request.method == "POST":
        if 'logout_btn' in request.POST:
            logout(request)
            return redirect('login_page')

        elif form.is_valid():
            category = form.cleaned_data["input_category"]
            amount = form.cleaned_data["input_amount"]
            date = form.cleaned_data["input_date"]
            new_expense_record = ExpenseDataModel(expense_category=category, expense_amount=amount,
                                                  expense_date=date, user=user)
            new_expense_record.save()

    form = home_form.HomeForm

    context = {
        'home_form': form,
        'user_id': user,
    }
    return render(request, "home.html", context)


def user_logout(request):
    logout(request)
    return redirect("login.html")


def view_expense(request):
    context = {}
    loggedin_user = request.user
    global expense_records
    if request.method == "POST":
        form = view_expense_form.ViewExpenseForm(request.POST)
        if form.is_valid():
            view_from_date = form.cleaned_data["expense_from_date"]
            view_to_date = form.cleaned_data["expense_to_date"]
            expense_records = ExpenseDataModel.objects.all().values().filter(user_id=loggedin_user.id)

            expense_data_all = []
            for entries in range(len(expense_records)):
                expense_data = []
                for keys in expense_records[entries]:
                    if keys == "expense_category":
                        expense_data.append(expense_records[entries][keys])
                    elif keys == "expense_amount":
                        expense_data.append(expense_records[entries][keys])
                    elif keys == "expense_date":
                        expense_data.append(expense_records[entries][keys])
                expense_data_all.append(expense_data)

            form = view_expense_form.ViewExpenseForm
            context = {
                "view_expense_form": form,
                "all_data": expense_data_all,
            }
    else:
        form = view_expense_form.ViewExpenseForm
        context = {
            "view_expense_form": form,

        }

    return render(request, "view_expense.html", context)

