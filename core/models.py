from django.db import models
from django.contrib.auth.models import User  

# Create your models here.

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='menu_items/')

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Optional: Associate booking with a user
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    number_of_people = models.PositiveIntegerField()
    date = models.DateField()
    time = models.TimeField()
    special_requests = models.TextField(blank=True, null=True)  # Optional field for special requests

    def __str__(self):
        return f"Booking for {self.full_name} on {self.date} at {self.time}"        

class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="staff_profile")
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='staff_profiles/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.position}"
