from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, time

# MenuItem Model
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='menu_items/')
    CATEGORY_CHOICES = [
        ('Starters', 'Starters'),
        ('Mains', 'Main Courses'),
        ('Desserts', 'Desserts'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Starters')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Add custom save logic if required, for example, ensure price is not negative
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        super(MenuItem, self).save(*args, **kwargs)


# Booking Model
class Booking(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    number_of_people = models.IntegerField()
    date = models.DateField()
    time = models.TimeField()
    special_requests = models.CharField(max_length=255, blank=True, default="")

    def __str__(self):
        return f"Booking for {self.full_name} on {self.date}"

    def clean(self):
        # Ensure the time field is not None
        if self.time is None:
            raise ValidationError("Time cannot be empty.")
        
        # Combine date and time into a timezone-aware datetime object
        try:
            reservation_datetime = timezone.make_aware(datetime.combine(self.date, self.time), timezone.get_current_timezone())
        except TypeError:
            raise ValidationError("The reservation time cannot be empty.")
        
        # Get current datetime as timezone-aware
        current_time = timezone.now()

        # Debug: Check reservation datetime and current time
        print(f"Reservation datetime: {reservation_datetime}")
        print(f"Current time: {current_time}")

        # Check if the reservation time is in the past
        if reservation_datetime < current_time:
            raise ValidationError("The reservation time cannot be in the past.")


# StaffProfile Model
class StaffProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    position = models.CharField(max_length=100, blank=False, default="Not Provided")  # Default to avoid NULL
    phone_number = models.CharField(max_length=15, blank=False, default="Not Provided")  # Default phone number
    address = models.CharField(max_length=255, blank=False, default="Not Provided")  # Default address
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # Keep null=True for optional picture
    department = models.CharField(max_length=100, choices=[
        ('Kitchen', 'Kitchen'),
        ('Service', 'Service'),
        ('Management', 'Management'),
        ('Front Desk', 'Front Desk'),
    ], blank=True, default='Service')  # Optional department for better organization

    def __str__(self):
        return f"Profile for {self.user.username}"

    def save(self, *args, **kwargs):
        # Add any validation logic, e.g., check phone number format or address length
        super(StaffProfile, self).save(*args, **kwargs)
