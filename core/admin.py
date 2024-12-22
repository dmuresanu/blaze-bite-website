from django.contrib import admin
from .models import MenuItem

# Register your models here.

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')  # Customize admin list view if needed
    search_fields = ('name', 'description')  # Add search functionality to the admin