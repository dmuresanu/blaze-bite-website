from django.shortcuts import render, redirect
from .forms import MenuItemForm
from .models import MenuItem
from .forms import BookingForm

# Create your views here.

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
            form.save()  # Save the booking to the database
            return redirect('booking_success')  # Redirect to a booking success page
    else:
        form = BookingForm()

    return render(request, 'core/booking.html', {'form': form}) 

def booking_success(request):
    return render(request, 'core/booking_success.html')       