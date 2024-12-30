from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.forms import UserChangeForm
from .forms import MenuItemForm, BookingForm, ContactForm
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

@login_required
def staff_profile(request):
    # Retrieve the menu items
    menu_items = MenuItem.objects.all()  # This can be filtered if necessary (e.g., only items created by the staff member)
    
    return render(request, 'registration/staff_profile.html', {'menu_items': menu_items})    

# Menu items should be accessible without login
def menu(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'menu.html', {'menu_items': menu_items})

def about(request):
    return render(request, 'about.html')

# Updated contact view to handle form submission

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                # Sending email to the restaurant
                send_mail(
                    'New Contact Form Submission',
                    form.cleaned_data['message'],
                    form.cleaned_data['email'],
                    ['restaurant@example.com'],
                    fail_silently=False,
                )

                # Sending confirmation email to the user
                send_mail(
                    'Thank you for your message',
                    'We have received your message and will get back to you soon.',
                    'no-reply@example.com',
                    [form.cleaned_data['email']],
                    fail_silently=False,
                )

                # After a successful form submission, redirect to the confirmation page
                return redirect('confirmation')  # Redirect to the confirmation page

            except Exception as e:
                return HttpResponse(f"An error occurred while sending the email: {e}")
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

def confirmation(request):
    return render(request, 'contact/confirmation.html')    

# Booking pages should be accessible without login, as you don't require authentication for bookings
def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Save the booking data
            booking = form.save()

            # Get the user's email and booking details
            user_email = form.cleaned_data['email']
            booking_details = f"Booking details:\n\nName: {form.cleaned_data['name']}\nEmail: {user_email}\nDate: {form.cleaned_data['date']}\nTime: {form.cleaned_data['time']}\nNumber of people: {form.cleaned_data['number_of_people']}"

            try:
                # Send email to the restaurant with the booking details
                send_mail(
                    'New Booking Confirmation',
                    booking_details,
                    user_email,  # Sender is the user
                    ['restaurant@example.com'],  # Recipient is the restaurant
                    fail_silently=False,
                )

                # Send confirmation email to the user
                send_mail(
                    'Booking Confirmation',
                    f'Thank you for your booking!\n\n{booking_details}\n\nWe will confirm your reservation soon.',
                    'no-reply@example.com',  # This is the sender email (no-reply)
                    [user_email],  # Recipient is the user
                    fail_silently=False,
                )

                # Success message
                messages.success(request, 'Your booking has been successfully made!')

                # Redirect to the booking success page
                return redirect('booking_success')

            except Exception as e:
                messages.error(request, f"An error occurred while sending the email: {e}")
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
            return redirect('index')  # Redirect to homepage or any other pag
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('index')  # Redirect to homepage or login page after logout
