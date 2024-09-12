from time import strftime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from expense_tracker_app.forms import login_form, register_form, home_form, view_expense_form, edit_expense_form
from expense_tracker_app.models import ExpenseDataModel
from datetime import date, datetime


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
            # Getting the data from request form
            view_from_date = form.cleaned_data["expense_from_date"]
            view_to_date = form.cleaned_data["expense_to_date"]
            # Converting input date to String for filtering purpose
            view_from_date = view_from_date.strftime('%Y-%m-%d')
            view_to_date = view_to_date.strftime('%Y-%m-%d')
            expense_records = ExpenseDataModel.objects.all().values().filter(user_id=loggedin_user.id,
                                                                             expense_date__range=[view_from_date,
                                                                                                  view_to_date])

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


def edit_expense(request):
    context = {}
    current_user = request.user
    if request.method == "POST":
        form = edit_expense_form.EditExpenseForm(request.POST)

        if "submit_updated_expense_details" in request.POST:
            updated_expense_id = request.POST['expense_record_id']
            updated_expense_category = request.POST["expense_category"]
            updated_expense_amount = request.POST["expense_amount"]
            updated_expense_date = request.POST["expense_date"]

            all_expense_id = ExpenseDataModel.objects.all().values().filter(id=updated_expense_id)

            context = {
                "edit_expense_form": form,
                "selected_record": updated_expense_id,
            }

        if "submit_to_view_expense_record" in request.POST:
            if form.is_valid():
                # Getting the data from request form
                edit_from_date = form.cleaned_data["expense_from_date"]
                edit_to_date = form.cleaned_data["expense_to_date"]
                # Converting input date to String for filtering purpose
                edit_from_date = edit_from_date.strftime('%Y-%m-%d')
                edit_to_date = edit_to_date.strftime('%Y-%m-%d')
                edit_expense_records = ExpenseDataModel.objects.all().values().filter(user_id=current_user.id,
                                                                             expense_date__range=[edit_from_date,
                                                                                                  edit_to_date])
                edit_expense_data_all = []
                for entries in range(len(edit_expense_records)):
                    edit_expense_data = []
                    for keys in edit_expense_records[entries]:
                        if keys == "expense_category":
                            edit_expense_data.append(edit_expense_records[entries][keys])
                        elif keys == "expense_amount":
                            edit_expense_data.append(edit_expense_records[entries][keys])
                        elif keys == "expense_date":
                            edit_expense_data.append(edit_expense_records[entries][keys])
                        elif keys == "id":
                            edit_expense_data.append(edit_expense_records[entries][keys])
                    edit_expense_data_all.append(edit_expense_data)

                form = edit_expense_form.EditExpenseForm
                context = {
                    "edit_expense_form": form,
                    "all_data": edit_expense_data_all,
                }
    else:
        form = edit_expense_form.EditExpenseForm
        context = {
            "edit_expense_form": form,
        }
    return render(request, "edit_expense.html", context)


def update_expense_data(request):
    form = edit_expense_form.EditExpenseForm
    context = {}


    return render(request, "edit_expense.html", context)
