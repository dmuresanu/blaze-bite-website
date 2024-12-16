from django.shortcuts import render
from .models import MenuItem

# Create your views here.

def index(request):
    return render(request, 'index.html')

def menu(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'menu.html', {'menu_items': menu_items})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')