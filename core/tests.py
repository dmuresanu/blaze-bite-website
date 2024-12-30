from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import date, time
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io
from .models import MenuItem
from .models import Booking

class MenuItemTestCase(TestCase):
    
    def setUp(self):
        # Create an in-memory image for testing
        image = Image.new('RGB', (100, 100), color=(255, 255, 255))
        image_file = io.BytesIO()
        image.save(image_file, format='JPEG')
        image_file.name = 'test_image.jpg'
        image_file.seek(0)

        # Create a MenuItem with the image
        self.menu_item = MenuItem.objects.create(
            name="Burger", 
            price=10.99, 
            description="Delicious burger", 
            image=SimpleUploadedFile(image_file.name, image_file.read(), content_type="image/jpeg")
        )

    def test_menu_item_creation(self):
        # Test that the menu item was created correctly
        self.assertEqual(self.menu_item.name, "Burger")
        self.assertEqual(self.menu_item.price, 10.99)
        self.assertEqual(self.menu_item.description, "Delicious burger")
        self.assertTrue(self.menu_item.image)  # Ensure the image is associated

    def test_menu_page_renders(self):
        # Test that the menu page renders correctly
        response = self.client.get(reverse("menu"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Menu")
        self.assertContains(response, "Burger")  # Ensure the menu item is displayed

class BookingTestCase(TestCase):

    def test_booking_form_submission(self):
        # Simulate a form submission (without email functionality)
        response = self.client.post(reverse('booking'), {
            'full_name': 'John Doe',
            'email': 'johndoe@example.com',
            'phone_number': '1234567890',
            'date': '2024-12-25',
            'time': '19:00'
        })
        
        # Check if the booking is created and redirected correctly
        self.assertEqual(response.status_code, 302)  # 302 means redirect
        self.assertRedirects(response, reverse('booking_success'))  # Check if redirected to success page
        self.assertEqual(Booking.objects.count(), 1)  # Ensure one booking was created        

# Create a booking object with a date and time in the future
future_booking = Booking(
    full_name="John Doe",
    email="john@example.com",
    phone_number="1234567890",
    number_of_people=4,
    date=date(2024, 12, 25),
    time=time(14, 30)
)

# Attempt to save the booking
future_booking.save()  # This should work if the date/time is in the future

# Try creating a booking with a past time
past_booking = Booking(
    full_name="Jane Doe",
    email="jane@example.com",
    phone_number="0987654321",
    number_of_people=2,
    date=date(2023, 12, 25),
    time=time(14, 30)
)

# Attempt to save the booking
past_booking.save()  # This should raise a ValidationError
