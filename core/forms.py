# core/forms.py
from django import forms
from .models import MenuItem
from .models import Booking

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price', 'image']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['full_name', 'email', 'phone_number', 'number_of_people', 'date', 'time', 'special_requests']