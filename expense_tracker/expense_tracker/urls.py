"""
URL configuration for expense_tracker project.

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
from django.urls import path, include
from expense_tracker_app import views

urlpatterns = [
    #path("expense_tracker_app/", include("expense_tracker_app.urls")),
    path('admin/', admin.site.urls),
    path('', views.user_login, name="login_page"),
    path('register.html', views.register_user, name="register_page"),
    path('home.html', views.home_page, name="home_page"),
    path('view_expense.html', views.view_expense, name="view_expense_page"),
]
