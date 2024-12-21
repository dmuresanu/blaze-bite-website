# core/forms.py
from django import forms
from .models import MenuItem, Booking
import datetime

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price', 'image']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['full_name', 'email', 'phone_number', 'number_of_people', 'date', 'time', 'special_requests']
    
    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date < datetime.date.today():
            raise forms.ValidationError('The reservation date cannot be in the past.')
        return date
    
    def clean_time(self):
        time = self.cleaned_data.get('time')
        if time < datetime.datetime.now().time():
            raise forms.ValidationError('The reservation time cannot be in the past.')
        return time
