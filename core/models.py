from django.db import models

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='menu_items/')

    def __str__(self):
        return self.name

class Booking(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    number_of_people = models.IntegerField()
    date = models.DateField()
    time = models.TimeField()
    special_requests = models.CharField(max_length=255, blank=True, default="")  # Default value for special requests

    def __str__(self):
        return f"Booking for {self.full_name} on {self.date}"

class StaffProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    position = models.CharField(max_length=100, blank=False, default="Not Provided")  # Default to avoid NULL
    phone_number = models.CharField(max_length=15, blank=False, default="Not Provided")  # Default phone number
    address = models.CharField(max_length=255, blank=False, default="Not Provided")  # Default address
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # Keep null=True for optional picture

    def __str__(self):
        return f"Profile for {self.user.username}"
