from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Category, Customers, Orders, Product
from django.contrib.sessions.models import Session


# Function to display home page
def home_page(request):
    # Get all the categories and products list
    category_list = Category.objects.values_list("category_name", flat=True)
    product_list = Product.objects.all().values()
    context = {}
    # Check if the user is logged in
    user_status = request.user.is_authenticated
    user_name = request.user.get_username()
    items_in_cart = 0
    if user_name != "":
        user_id = Customers.objects.all().values_list('id', flat=True).get(username=user_name)
        products_selected = Orders.objects.all().values_list('product_id', flat=True).filter(customer_id=user_id)
        each_item_status = []

        for items in products_selected:
            each_item_status = Orders.objects.all().values_list('status', flat=True).filter(product_id=items,
                                                                                            customer_id=user_id)
            if each_item_status[0] == "New":
                items_in_cart = items_in_cart + 1

    # Logic to display categories based on the option selected and rendering new page with the details required
    if request.method == "POST":
        if 'category_name' in request.POST:
            category_option = request.POST['category_name']
            categories_id = Category.objects.all().values_list('id', flat=True).get(category_name=category_option)

            if categories_id != 4:
                filtered_products = Product.objects.all().values().filter(category_id=categories_id)
                context = {
                    'category_option': category_option,
                    'cat_id': categories_id,
                    'filtered_prod': filtered_products,
                    'category_lists': category_list,
                    'user_status': user_status,
                    'username': user_name,
                    'items_in_cart': items_in_cart,
                }
            elif categories_id == 4:
                filtered_products = product_list
                context = {
                    'cat_id': categories_id,
                    'category_lists': category_list,
                    'filtered_prod': filtered_products,
                    'user_status': user_status,
                    'username': user_name,
                    'items_in_cart': items_in_cart,
                }
        elif 'add_item' in request.POST:
            add_prod_id = request.POST['add_item']
            add_prod_id = str(add_prod_id)
            add_prod_id = add_prod_id.split('_')[0]
            user_id = Customers.objects.all().values_list('id', flat=True).get(username=user_name)
            category_num = Product.objects.all().values_list('category', flat=True).get(id=add_prod_id)
            filtered_products = Product.objects.all().values().filter(category_id=category_num)
            existing_product = Orders.objects.filter(product=add_prod_id).exists()
            user_exist = Orders.objects.all().values_list('customer_id', flat=True).filter(product_id=add_prod_id)

            if existing_product is True and user_id in user_exist:
                item_quantity = Orders.objects.all().values_list('quantity', flat=True).get(product=add_prod_id,
                                                                                            customer_id=user_id)
                item_quantity = item_quantity + 1
                item_record = Orders.objects.get(product=add_prod_id, customer_id=user_id)
                item_record.quantity = item_quantity
                item_record.save()
            else:
                product_object = Product.objects.get(id=add_prod_id)
                customer_name = request.user.get_username()
                customer_obj = Customers.objects.get(username=customer_name)
                quantity = 1
                add_product_record = Orders(quantity=quantity, customer=customer_obj, product=product_object,
                                            status="New")
                add_product_record.save()
            context = {
                'category_lists': category_list,
                'product_list': product_list,
                'user_status': user_status,
                'username': user_name,
                'filtered_prod': filtered_products,
                'items_in_cart': items_in_cart,
            }
        elif 'remove_item' in request.POST:
            remove_prod_id = request.POST['remove_item']
            remove_prod_id = str(remove_prod_id)
            remove_prod_id = remove_prod_id.split('_')[0]
            category_num = Product.objects.all().values_list('category', flat=True).get(id=remove_prod_id)
            filtered_products = Product.objects.all().values().filter(category_id=category_num)
            existing_product = Orders.objects.filter(product=remove_prod_id).exists()
            user_id = Customers.objects.all().values_list('id', flat=True).get(username=user_name)
            user_exist = Orders.objects.all().values_list('customer_id', flat=True).filter(product_id=remove_prod_id)
            if existing_product is True and user_id in user_exist:
                item_quantity = Orders.objects.all().values_list('quantity', flat=True).get(product=remove_prod_id,
                                                                                            customer_id=user_id)
                item_quantity = item_quantity - 1
                item_record = Orders.objects.get(product=remove_prod_id, customer_id=user_id)
                item_record.quantity = item_quantity
                item_record.save()

            context = {
                'category_lists': category_list,
                'product_list': product_list,
                'user_status': user_status,
                'username': user_name,
                'filtered_prod': filtered_products,
                'items_in_cart': items_in_cart,
            }

        return render(request, 'home.html', context)
    else:
        filtered_products = Product.objects.all().values()
        context = {
            'category_lists': category_list,
            'product_list': product_list,
            'filtered_prod': filtered_products,
            'user_status': user_status,
            'username': user_name,
            'items_in_cart': items_in_cart,
        }
        return render(request, 'home.html', context)


# Function for signing up
def signup(request):
    # Logic to post the data to server and saving it into database
    if request.method == 'POST':
        cust_name = request.POST['user_name']
        cust_email = request.POST['email_id']
        cust_password = request.POST['pwd']
        cust_address = request.POST['cust_address']
        cust_contact = request.POST['contact_no']
        # Saving data to database
        new_cust_record = Customers(username=cust_name, email=cust_email, password=cust_password, address=cust_address,
                                    contact=cust_contact)
        new_cust_record.save()
        new_user = User.objects.create_user(cust_name, cust_email, cust_password)
        new_user.save()

        context = {
            'name': cust_name,
            'email': cust_email,
            'password': cust_password,
            'address': cust_address,
            'contact': cust_contact,
        }
        return HttpResponseRedirect("signup.html")
    else:
        return render(request, "signup.html")


# Function to log in
def login_fun(request):
    # Send credentials for authentication
    if request.method == 'POST':
        username_to_verify = request.POST['username']
        password_to_verify = request.POST['password']
        # Authenticate the credentials from auth.user table
        user = authenticate(request, username=username_to_verify, password=password_to_verify)
        # If user exists, do log in
        if user is not None:
            login(request, user)
            return redirect("home_page")
    else:
        return render(request, "login.html")


# Function to log out
def logout_user(request):
    logout(request)
    return redirect("home_page")


def update_cart(request):
    user_status = request.user.is_authenticated
    if request.method == 'POST':
        if not user_status:
            return redirect("signup_page")
        elif user_status:
            return redirect("home_page")


def display_cart(request):
    user_name = request.user.get_username()
    user_id = Customers.objects.all().values_list('id', flat=True).get(username=user_name)
    products_selected = Orders.objects.all().values_list('product_id', flat=True).filter(customer_id=user_id)
    item_record = []
    all_items_total = 0
    pending_status_flag = False
    each_item_status = []

    if request.method == 'POST':
        if 'checkout_button' in request.POST:
            for prod in products_selected:
                current_order_object = Orders.objects.get(product_id=prod, customer_id=user_id)
                current_order_object.status = "Pending"
                current_order_object.save()

    for p in products_selected:
        each_item_status = Orders.objects.all().values_list('status', flat=True).filter(product_id=p,
                                                                                        customer_id=user_id)
        if each_item_status[0] == "New":
            item_details = []
            item_details.append(p)
            item_details.append(Product.objects.all().values_list('product_name', flat=True).get(id=p))
            item_details.append(Product.objects.all().values_list('images', flat=True).get(id=p))
            item_details.append(
                Orders.objects.all().values_list('quantity', flat=True).get(product_id=p, customer_id=user_id))
            p_quantity = Orders.objects.all().values_list('quantity', flat=True).get(product_id=p, customer_id=user_id)
            each_p_price = Product.objects.all().values_list('price', flat=True).get(id=p)
            total_p_price = p_quantity * each_p_price
            all_items_total = all_items_total + total_p_price
            item_details.append(total_p_price)
            item_record.append(item_details)
    context = {
        'products_selected': products_selected,
        'item_record': item_record,
        'all_items_price': all_items_total,
        'each_item_status': each_item_status,
        'pending_status_flag': pending_status_flag,
    }
    return render(request, "cart.html", context)


def display_order(request):
    user_name = request.user.get_username()
    user_id = Customers.objects.all().values_list('id', flat=True).get(username=user_name)
    products_selected = Orders.objects.all().values_list('product_id', flat=True).filter(customer_id=user_id)
    item_record = []
    all_items_total = 0
    for p in products_selected:
        each_item_status = Orders.objects.all().values_list('status', flat=True).filter(product_id=p,
                                                                                        customer_id=user_id)
        if each_item_status[0] == "Pending":
            item_details = []
            item_details.append(p)
            item_details.append(Product.objects.all().values_list('product_name', flat=True).get(id=p))
            item_details.append(Product.objects.all().values_list('images', flat=True).get(id=p))
            item_details.append(
                Orders.objects.all().values_list('quantity', flat=True).get(product_id=p, customer_id=user_id))
            p_quantity = Orders.objects.all().values_list('quantity', flat=True).get(product_id=p, customer_id=user_id)
            each_p_price = Product.objects.all().values_list('price', flat=True).get(id=p)
            total_p_price = p_quantity * each_p_price
            all_items_total = all_items_total + total_p_price
            item_details.append(total_p_price)
            item_details.append(
                Orders.objects.all().values_list('status', flat=True).get(product_id=p, customer_id=user_id))
            item_record.append(item_details)

    context = {
        'products_selected': products_selected,
        'item_record': item_record,
        'all_items_price': all_items_total,
    }

    return render(request, "order.html", context)
