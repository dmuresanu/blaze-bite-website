from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io
from .models import MenuItem

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

