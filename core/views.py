from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserChangeForm
from .forms import MenuItemForm, BookingForm
from .models import MenuItem, Booking

def index(request):
    return render(request, 'index.html')

# View for adding a menu item, restricted to staff members only
@login_required
def add_menu_item(request, item_id=None):
    # Check if the user is staff, else redirect to a different page
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to add menu items.")
        return redirect('staff_profile')  # Redirect to profile or another page

    if item_id:
        item = get_object_or_404(MenuItem, id=item_id)
        form = MenuItemForm(request.POST or None, request.FILES or None, instance=item)
    else:
        form = MenuItemForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Menu item saved successfully!')
        return redirect('menu')

    return render(request, 'add_menu_item.html', {'form': form, 'item_id': item_id})

# Protect delete_menu_item view with login_required as well
@login_required
def delete_menu_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    item.delete()
    messages.success(request, 'Menu item deleted successfully!')
    return redirect('menu')

# The staff_profile and edit_profile views are also protected by login_required
@login_required
def staff_profile(request):
    return render(request, 'registration/staff_profile.html')

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

# Menu items should be accessible without login
def menu(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'menu.html', {'menu_items': menu_items})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

# Booking pages should be accessible without login, as you don't require authentication for bookings
def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your booking has been successfully made!')
            return redirect('booking_success')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookingForm()

    return render(request, 'booking.html', {'form': form})

def booking_success(request):
    return render(request, 'booking_success.html')


# Login and logout views
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')  # Redirect to homepage or any other page
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('index')  # Redirect to homepage or login page after logout
