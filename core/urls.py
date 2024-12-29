# core/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('booking/', views.booking, name='booking'),
    path('booking/success/', views.booking_success, name='booking_success'),
    path('menu/', views.menu, name='menu'),
    path('menu/add/', views.add_menu_item, name='add_menu_item'),
    path('menu/edit/<int:item_id>/', views.add_menu_item, name='edit_menu_item'),
    path('menu/delete/<int:item_id>/', views.delete_menu_item, name='delete_menu_item'),
    path('staff/profile/', views.staff_profile, name='staff_profile'),
    path('staff/edit-profile/', views.edit_profile, name='edit_profile'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.user_login, name='login'),  # Custom login view
    path('logout/', views.user_logout, name='logout'),  # Custom logout view
]
