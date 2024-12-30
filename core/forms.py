# forms.py
from django import forms
from .models import MenuItem, Booking, StaffProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
import datetime

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['category','name', 'description', 'price', 'image']

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
        date = self.cleaned_data.get('date')
        
        # Combine the provided date and time into a datetime object
        reservation_datetime = timezone.make_aware(datetime.datetime.combine(date, time), timezone.get_current_timezone())

        # Get the current datetime (timezone-aware)
        current_time = timezone.now()

        # Debug: Check the reservation datetime and current time
        print(f"Reservation datetime: {reservation_datetime}")
        print(f"Current time: {current_time}")

        # Check if the reservation time is in the past
        if reservation_datetime < current_time:
            raise forms.ValidationError('The reservation time cannot be in the past.')

        return time


class StaffUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')  # Don't include password in fields here

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()

            # Create StaffProfile after the user is saved and committed
            StaffProfile.objects.create(user=user)

        return user

class ContactForm(forms.Form):
    CONTACT_REASONS = [
        ('inquiry', 'Inquiry'),
        ('reservation', 'Reservation'),
    ]
    
    name = forms.CharField(max_length=100, required=True, label='Your Name')
    email = forms.EmailField(required=True, label='Your Email')
    message = forms.CharField(widget=forms.Textarea, required=True, label='Message')
    reason = forms.ChoiceField(choices=CONTACT_REASONS, required=True, label='Reason for Contacting')