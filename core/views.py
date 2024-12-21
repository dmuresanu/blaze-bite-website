from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import MenuItemForm, BookingForm
from .models import MenuItem, Booking
import datetime

# Function to send booking confirmation email
def send_booking_confirmation_email(booking):
    subject = f"Booking Confirmation - {booking.full_name}"
    message = f"Dear {booking.full_name},\n\nYour table has been successfully booked for {booking.date} at {booking.time}.\n\nBest regards,\nRestaurant Team"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [booking.email, settings.RESTAURANT_EMAIL]  # Sends to user and restaurant
    send_mail(subject, message, from_email, recipient_list)

def index(request):
    return render(request, 'index.html')

def add_menu_item(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('menu')  # Redirect to the menu page after successful form submission
    else:
        form = MenuItemForm()
    return render(request, 'add_menu_item.html', {'form': form})

def menu(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'menu.html', {'menu_items': menu_items})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Save the form and send confirmation email
            booking = form.save()
            send_booking_confirmation_email(booking)
            messages.success(request, 'Your booking has been successfully made!')
            return redirect('booking_success')  # Redirect to a booking success page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookingForm()

    return render(request, 'booking.html', {'form': form})

def booking_success(request):
    return render(request, 'booking_success.html')
