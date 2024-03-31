from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('signup.html', views.signup, name='signup_page'),
    path('login.html', views.login_fun, name='login_page'),
    path('', views.logout_user, name='logout_page'),
    path('logout.html', views.logout_user, name='logout_page'),
    path('', views.update_cart, name='update_cart'),
    path('cart.html', views.display_cart, name='cart_page'),
    path('order.html', views.display_order, name='order_page'),
]