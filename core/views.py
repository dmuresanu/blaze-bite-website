from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import MenuItemForm, BookingForm
from .models import MenuItem, Booking

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
    print(menu_items)  # Debugging line
    return render(request, 'menu.html', {'menu_items': menu_items})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def booking(request):
    if request.method == 'POST':
        print("POST request received")  # Debug log
        form = BookingForm(request.POST)
        if form.is_valid():
            print("Form is valid")  # Debug log
            booking = form.save()

            messages.success(request, 'Your booking has been successfully made!')
            return redirect('booking_success')  # Redirect to a booking success page
        else:
            print("Form is invalid:", form.errors)  # Debug log
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookingForm()

    return render(request, 'booking.html', {'form': form})

def booking_success(request):
    return render(request, 'booking_success.html')
