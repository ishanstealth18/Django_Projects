"""
URL configuration for e_library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from e_library_app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home_page"),
    path('register.html', views.register, name="register_page"),
    path('login.html', views.login_fun, name="login_page"),
    path('logout.html', views.logout_fun, name="logout_page"),
    path('add_book.html', views.add_book, name="addbook_page"),
    path('contribute.html', views.contribute, name="contribute_page"),
    path('edit_book_details/<int:book_id>/', views.edit_book, name="edit_book_details_page"),
    path('view_book_details/<int:book_id>/', views.view_book, name="view_book_details_page"),

]
