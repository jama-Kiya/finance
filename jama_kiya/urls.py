from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_registration, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('add-customer/', views.add_customer, name='add_customer'),
    path('customer/<int:id>/', views.customer_detail, name='customer_detail'),
]