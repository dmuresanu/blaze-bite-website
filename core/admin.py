from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django import forms
from django.contrib import admin
from .models import MenuItem
from .models import StaffProfile

# Unregister the default User admin to avoid the 'AlreadyRegistered' error
admin.site.unregister(User)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')  # Customize admin list view if needed
    search_fields = ('name', 'description')  # Add search functionality to the admin

class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'phone_number', 'address', 'profile_picture')
    search_fields = ('user__username', 'position')
    list_filter = ('position',)

# Register StaffProfile with its admin
admin.site.register(StaffProfile, StaffProfileAdmin)    

# Create a form for User with additional staff profile fields
class StaffUserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

        # Create staff profile after saving user
        StaffProfile.objects.create(user=user)

        return user

class StaffUserAdmin(UserAdmin):
    add_form = StaffUserCreationForm
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name'),
        }),
    )

# Register custom User admin
admin.site.register(User, StaffUserAdmin)
