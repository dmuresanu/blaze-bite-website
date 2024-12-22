from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import MenuItem, StaffProfile
from .forms import StaffUserCreationForm  # Ensure this form handles password1 and password2

# Unregister the default User admin to avoid the 'AlreadyRegistered' error
admin.site.unregister(User)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')
    search_fields = ('name', 'description')  # Add search functionality to the admin

class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'phone_number', 'address', 'profile_picture')
    search_fields = ('user__username', 'position')
    list_filter = ('position',)

# Register StaffProfile with its admin
admin.site.register(StaffProfile, StaffProfileAdmin)

class StaffUserAdmin(UserAdmin):
    # Use the custom form for creating users
    add_form = StaffUserCreationForm
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    
    # Define the fieldsets for editing existing users
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}), 
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Define the fieldsets for adding new users
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'is_staff', 'is_active'),
        }),
    )
    
    # Define search functionality
    search_fields = ('username', 'email')
    ordering = ('username',)

# Register custom User admin
admin.site.register(User, StaffUserAdmin)
