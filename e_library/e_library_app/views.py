from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms.register_form import RegisterForm
from .forms.login_form import LoginForm
from django.contrib.auth.models import User
from .models import RegisterModel, AddBookModel
from .forms.addbooks_form import AddBooksForm
from .forms.editbooks_form import EditBooksForm
from .forms.viewbooks_form import ViewBooksForm

# Create your views here.


def home(request):
    user_authenticated = request.user.is_authenticated
    current_username = request.user.get_username()
    context = {
        "user_authenticated": user_authenticated,
        "current_user": current_username,
    }
    return render(request, 'home.html', context)


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email_address"]
            password = form.cleaned_data["password"]
            customer_record = RegisterModel(last_name=last_name, email_address=email, password=password,
                                            first_name=first_name)
            customer_record.save()
            new_customer_record = User.objects.create_user(username=first_name, first_name=first_name, email=email,
                                                           password=password, last_name=last_name)
            new_customer_record.save()

    form = RegisterForm
    context = {
        'form': form,
    }
    return render(request, 'register.html', context)


def login_fun(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data["login_email_address"]
            user_password = login_form.cleaned_data["login_password"]
            user = authenticate(request, username=user_email, password=user_password)
            if user is not None:
                login(request, user)
        return redirect("home_page")
    else:
        login_form = LoginForm
        login_flag = request.user.is_authenticated
        user_name = request.user.get_username()
        context = {
            "form": login_form,
            'user': login_flag,
            'user_name': user_name,
        }
        return render(request, "login.html", context)


def logout_fun(request):
    logout(request)
    return redirect("home_page")


def add_book(request):
    form = AddBooksForm
    user_authentication = request.user.is_authenticated
    if user_authentication:
        current_user = request.user.get_username()
        if request.method == "POST":
            addbook_form = AddBooksForm(request.POST, request.FILES)
            if addbook_form.is_valid():
                book_title = addbook_form.cleaned_data["title"]
                book_summary = addbook_form.cleaned_data["summary"]
                book_pages = addbook_form.cleaned_data["pages"]
                book_pdf = addbook_form.cleaned_data["pdf"]
                book_category = addbook_form.cleaned_data["category"]
                new_book_record = AddBookModel(title=book_title, summary=book_summary, pages=book_pages, pdf=book_pdf,
                                               category=book_category, contributed_by=str(current_user))
                new_book_record.save()
            context = {
                'add_book_form': form,
                'current_user': current_user,
            }
        else:
            context = {
                'add_book_form': form,
                'current_user': current_user,
            }

        return render(request, "add_book.html", context)
    else:
        return redirect("login.html")


def contribute(request):
    id_list = []
    book_obj = AddBookModel.objects.all()
    all_books = []
    page_to_open = ""
    context = {}
    current_username = request.user.get_username()
    for obj in book_obj:
        all_books.append(obj)

    if request.method == "POST":
        if 'delete_book' in request.POST:
            book_id_received = int(request.POST["book_id"])
            all_book_id = AddBookModel.objects.all().values('id')
            for b_id in all_book_id:
                id_list.append(b_id.get('id'))
                if book_id_received in id_list:
                    AddBookModel.objects.get(id=book_id_received).delete()
                    break
            page_to_open = "contribute.html"
            context = {
                'book_obj': book_obj,
                'books': all_books,
                "current_user": current_username,
            }

    else:
        page_to_open = "contribute.html"
        context = {
            'book_obj': book_obj,
            'books': all_books,
            "current_user": current_username,
        }
    return render(request, page_to_open, context)


def edit_book(request, book_id):
    default_template = EditBooksForm

    if request.method == "POST":
        edit_book_form = EditBooksForm(request.POST, request.FILES)
        if "edit_book_details" in request.POST:
            if edit_book_form.is_valid():
                existing_book_data = AddBookModel.objects.get(id=book_id)
                existing_book_data.title = edit_book_form.cleaned_data["title"]
                existing_book_data.summary = edit_book_form.cleaned_data["summary"]
                existing_book_data.pages = edit_book_form.cleaned_data["pages"]
                existing_book_data.pdf = edit_book_form.cleaned_data["pdf"]
                existing_book_data.category = edit_book_form.cleaned_data["category"]
                existing_book_data.save()

            return redirect("contribute_page")

        elif 'edit_details' in request.POST:

            book_details = AddBookModel.objects.all().values().filter(id=book_id)
            pdf_name = request.FILES

            for k in book_details[0]:
                if k is 'pdf':
                    pdf_name = book_details[0][k]

            title = book_details[0].get('title')
            summary = book_details[0].get('summary')
            pages = book_details[0].get('pages')
            category = book_details[0].get('category')
            form = EditBooksForm(
                {'title': title, 'summary': summary, 'pages': pages, 'current_pdf': pdf_name,
                    'category': category})
            template_to_load = "edit_book_details.html"
            context = {
                "edit_book_form": form,
                "id_received": book_id,
                "template": template_to_load,
            }
            return render(request, "edit_book_details.html", context)

    else:
        template_to_load = "edit_book_details.html"
        context = {
            "edit_book_form": default_template,
        }
        return render(request, template_to_load, context)


def view_book(request, book_id):
    context = {}
    if request.method == "POST":
        book_details = AddBookModel.objects.all().values().filter(id=book_id)
        pdf_name = request.FILES

        for k in book_details[0]:
            if k is 'pdf':
                pdf_name = book_details[0][k]

        title = book_details[0].get('title')
        summary = book_details[0].get('summary')
        pages = book_details[0].get('pages')
        category = book_details[0].get('category')
        form = ViewBooksForm(
            {'title': title, 'summary': summary, 'pages': pages, 'current_pdf': pdf_name,
             'category': category})
        context = {
            "view_book_form": form,
        }
    return render(request, "view_book_details.html", context)
