from django.db import models

# MenuItem Model
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='menu_items/')

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
    special_requests = models.CharField(max_length=255, blank=True, default="")  # Default value for special requests

    def __str__(self):
        return f"Booking for {self.full_name} on {self.date}"

    def save(self, *args, **kwargs):
        # Ensure that the phone number has a valid format (you could use regex or phone validation library here)
        if len(self.phone_number) < 10:
            raise ValueError("Phone number is too short.")
        super(Booking, self).save(*args, **kwargs)


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
