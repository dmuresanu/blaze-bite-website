from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import MenuItemForm, BookingForm
from .models import MenuItem, Booking
from django.contrib.auth.forms import UserChangeForm

def index(request):
    return render(request, 'index.html')

@login_required
def add_menu_item(request, item_id=None):
    # If an item_id is provided, we fetch the existing MenuItem instance for editing
    if item_id:
        item = get_object_or_404(MenuItem, id=item_id)
        form = MenuItemForm(request.POST or None, request.FILES or None, instance=item)
    else:
        form = MenuItemForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Menu item saved successfully!')
        return redirect('menu')  # Redirect to the menu list page after saving

    return render(request, 'add_menu_item.html', {'form': form, 'item_id': item_id})

@login_required
def delete_menu_item(request, item_id):
    # Get the MenuItem object or 404 if not found
    item = get_object_or_404(MenuItem, id=item_id)
    
    # Delete the item and display a success message
    item.delete()
    messages.success(request, 'Menu item deleted successfully!')
    
    return redirect('menu')  # Redirect back to the menu page

@login_required
def staff_profile(request):
    # Show the current user's profile details
    return render(request, 'staff_profile.html')

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('staff_profile')
    else:
        form = UserChangeForm(instance=user)

    return render(request, 'edit_profile.html', {'form': form})

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
            booking = form.save()
            messages.success(request, 'Your booking has been successfully made!')
            return redirect('booking_success')  # Redirect to a booking success page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookingForm()

    return render(request, 'booking.html', {'form': form})

def booking_success(request):
    return render(request, 'booking_success.html')
