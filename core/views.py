from django.shortcuts import render, redirect
from .forms import MenuItemForm
from .models import MenuItem

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