from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from expense_tracker_app.forms import login_form, register_form, home_form, view_expense_form, edit_expense_form
from expense_tracker_app.models import ExpenseDataModel
from expense_tracker_app.services import data_training


# Create your views here.

# Function to register a user. This function will register new users to database.
def register_user(request):
    # Creating a form from data received in the request
    form = register_form.RegisterForm(request.POST)
    # Check if method is POST, form is valid and get data from the request
    if request.method == "POST":
        if form.is_valid():
            first_name = form.cleaned_data["register_firstname"]
            last_name = form.cleaned_data["register_lastname"]
            email = form.cleaned_data["register_email"]
            password = form.cleaned_data["register_password"]
            # Create a new user after getting data from the request
            new_user_record = User.objects.create_user(first_name=first_name, last_name=last_name, email=email,
                                                       password=password, username=first_name)
            # Save data to database
            new_user_record.save()

    # Creating a blank Register form without data from the request
    form = register_form.RegisterForm
    context = {
        "register_form": form,
    }
    return render(request, "register.html", context)


# Login function for a user. This will log in the user and create a session.
def user_login(request):
    form = login_form.LoginForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            user_name = form.cleaned_data["login_username"]
            user_password = form.cleaned_data["login_password"]
            # Validating user by using Authenticate function, this will authenticate user from User database mentioned
            # in Settings file
            validate_user = authenticate(request, username=user_name, password=user_password)
            if validate_user is not None:
                login(request, validate_user)
        return redirect("home.html")

    else:
        form = login_form.LoginForm
        context = {
            "login_form": form,
        }
        return render(request, "login.html", context)


# Function to display Home page
def home_page(request):
    form = home_form.HomeForm(request.POST)
    # Getting all the objects from database filtered by user ids
    user = User.objects.all().get(id=request.user.id)
    if request.method == "POST":

        if form.is_valid():
            category = form.cleaned_data["input_category"]
            amount = form.cleaned_data["input_amount"]
            date = form.cleaned_data["input_date"]
            description = form.cleaned_data["input_description"]
            # Creating a new record in Expense model with input data
            new_expense_record = ExpenseDataModel(expense_category=category, expense_amount=amount,
                                                  expense_date=date, expense_description=description, user=user)
            new_expense_record.save()
        else:
            # Creating a validation if input is null.
            raise ValidationError("Please check all the inputs are provided!!")

    form = home_form.HomeForm

    context = {
        'home_form': form,
        'user_id': user,
    }
    return render(request, "home.html", context)


# Logout function
def user_logout(request):
    logout(request)
    return redirect("login.html")


# Function to View Expenses, this function allows user to see expense in a given date range
def view_expense(request):
    context = {}
    # Getting the current user object
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
            # Getting the expense data using filter from Expense model
            expense_records = ExpenseDataModel.objects.all().values().filter(user_id=loggedin_user.id,
                                                                             expense_date__range=[view_from_date,
                                                                                                  view_to_date])

            expense_data_all = []
            total_expense_amount = 0.00
            # Creating a list of each record and passing it to HTML page
            for entries in range(len(expense_records)):
                expense_data = []
                for keys in expense_records[entries]:
                    if keys == "expense_category":
                        expense_data.append(expense_records[entries][keys])
                    elif keys == "expense_amount":
                        expense_data.append(expense_records[entries][keys])
                        total_expense_amount = total_expense_amount + float(expense_records[entries][keys])
                    elif keys == "expense_date":
                        expense_data.append(expense_records[entries][keys])
                    elif keys == "expense_description":
                        expense_data.append(expense_records[entries][keys])
                expense_data_all.append(expense_data)

            form = view_expense_form.ViewExpenseForm
            context = {
                "view_expense_form": form,
                "all_data": expense_data_all,
                "total_expense_amount": round(total_expense_amount, 2),
            }
    else:
        form = view_expense_form.ViewExpenseForm
        context = {
            "view_expense_form": form,

        }
    return render(request, "view_expense.html", context)


# function to Edit expense. This function updates any existing record within given range and can dlete the record as
# well from database
def edit_expense(request):
    context = {}
    current_user = request.user
    if request.method == "POST":
        # If delete button is pressed, record will be deleted from database
        if "delete_expense_details" in request.POST:
            delete_record_id = request.POST["delete_record_id"]
            expense_record_obj = ExpenseDataModel.objects.get(id=delete_record_id)
            expense_record_obj.delete()
            form = edit_expense_form.EditExpenseForm(request.POST)

            context = {
                "edit_expense_form": form,
            }
        # If Expense details are updated, database will be updated with new details
        if "submit_updated_expense_details" in request.POST:
            # Getting all the updated data from the request
            updated_expense_id = request.POST["record_id"]
            updated_expense_category = request.POST["expense_category"]
            updated_expense_description = request.POST["expense_description"]
            updated_expense_amount = request.POST["expense_amount"]
            updated_expense_date = request.POST["expense_date"]
            # Updating the database with new data
            all_expense_id = ExpenseDataModel.objects.get(id=updated_expense_id)
            all_expense_id.expense_category = updated_expense_category
            all_expense_id.expense_description = updated_expense_description
            all_expense_id.expense_amount = updated_expense_amount
            all_expense_id.expense_date = updated_expense_date
            all_expense_id.save()
            form = edit_expense_form.EditExpenseForm

            context = {
                "edit_expense_form": form,
            }
        # View data from database
        total_expense_amount = 0.00
        if "submit_to_view_expense_record" in request.POST:
            form = edit_expense_form.EditExpenseForm(request.POST)
            if form.is_valid():
                # Getting the data from request form
                edit_from_date = form.cleaned_data["expense_from_date"]
                edit_to_date = form.cleaned_data["expense_to_date"]
                # Converting input date to String for filtering purpose
                edit_from_date = edit_from_date.strftime('%Y-%m-%d')
                edit_to_date = edit_to_date.strftime('%Y-%m-%d')
                edit_expense_records = ExpenseDataModel.objects.all().values().filter(user_id=current_user.id,
                                                                                      expense_date__range=[
                                                                                          edit_from_date,
                                                                                          edit_to_date])
                edit_expense_data_all = []
                for entries in range(len(edit_expense_records)):
                    edit_expense_data = []
                    for keys in edit_expense_records[entries]:
                        if keys == "expense_category":
                            edit_expense_data.append(edit_expense_records[entries][keys])
                        elif keys == "expense_amount":
                            edit_expense_data.append(edit_expense_records[entries][keys])
                            total_expense_amount = total_expense_amount + float(edit_expense_records[entries][keys])
                        elif keys == "expense_date":
                            edit_expense_data.append(edit_expense_records[entries][keys])
                        elif keys == "id":
                            edit_expense_data.append(edit_expense_records[entries][keys])
                        elif keys == "expense_description":
                            edit_expense_data.append(edit_expense_records[entries][keys])
                    edit_expense_data_all.append(edit_expense_data)

                form = edit_expense_form.EditExpenseForm(request.POST)
                context = {
                    "edit_expense_form": form,
                    "all_data": edit_expense_data_all,
                    "total_expense_amount": round(total_expense_amount, 2),
                }
    else:
        form = edit_expense_form.EditExpenseForm
        context = {
            "edit_expense_form": form,
        }
    return render(request, "edit_expense.html", context)


# Creating function to view chart
def view_chart(request):
    context = {}
    current_user = request.user
    if request.method == "POST":
        expense_from_date = request.POST["from_date"]
        expense_to_date = request.POST["to_date"]
        # Getting values after filtering from Expense model. This will return dictionary of values
        expense_data = ExpenseDataModel.objects.values('expense_category', 'expense_amount').filter(
            user_id=current_user, expense_date__range=[expense_from_date, expense_to_date])
        expense_data_dict = {}

        # check if expense category already exist in the dictionary then append expense amount to Category key else
        # create new category and add expense amount as value to it
        for data in expense_data:
            if data['expense_category'] in expense_data_dict:
                expense_data_dict[data['expense_category']].append(data['expense_amount'])
            else:
                expense_data_dict[data['expense_category']] = [data['expense_amount']]
        # Create a dictionary of all expense categories with total expense amount for it
        expense_data_total_dict = {}
        total_expense_amount = 0
        sorted_total_expense = {}
        top_3_categories = {}
        for category in expense_data_dict:
            category_amount = 0
            for price in expense_data_dict[category]:
                category_amount = category_amount + float(price)
            expense_data_total_dict[category] = category_amount
            total_expense_amount = total_expense_amount + float(expense_data_total_dict[category])

        if len(expense_data_total_dict) >= 3:
            sorted_total_expense = sorted(expense_data_total_dict.items(), key=lambda i: i[1],  reverse=True)
            for x in range(3):
                top_3_categories[sorted_total_expense[x][0]] = sorted_total_expense[x][1]

        context = {
            "from_date": expense_from_date,
            "to_date": expense_to_date,
            "data": expense_data,
            "dict": expense_data_dict,
            "total": expense_data_total_dict,
            "total_expense_amount": round(total_expense_amount, 2),
            "sorted_expense_categories": sorted_total_expense,
            "top_3_category": top_3_categories,
        }

    return render(request, "view_chart.html", context)


def recommendations(request):
    context = {}
    if request.method == "POST":
        recommend_btn_id = request.POST["suggestion_btn"]

        # check if House Rent category is in top 3 monthly expense
        if "House Rent" in recommend_btn_id:
            # get user history browse data in to vector form after all processing
            browser_history_data = data_training.get_browser_data()
            # condition to check if user have previous browse history, calculate cos similarity between Title + Address
            # from given dataset and filtered data from user browse history
            if browser_history_data is not None:
                print("User has browser history!!! So recommendation based on user history data.")
                suggestion_list = data_training.user_history_title_cosine_similarity()

            # condition to check if user does not have previous browse history, calculate cos similarity between current
            # location and addresses from the dataset.
            else:
                print("User does not have any browser history!! So current location will be used for recommendation.")
                suggestion_list = data_training.find_address_cos_similarity()
            # create context and pass values
            context = {
                "btn_id": recommend_btn_id,
                "suggestions": suggestion_list,
            }

    return render(request, "top_recommendations.html", context)

