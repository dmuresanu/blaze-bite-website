# core/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import StaffProfile

@receiver(post_save, sender=User)
def create_staff_profile(sender, instance, created, **kwargs):
    if created:
        # Automatically create a StaffProfile when a new User is created
        StaffProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_staff_profile(sender, instance, **kwargs):
    # Save the StaffProfile when the User is saved
    if hasattr(instance, 'staff_profile'):
        instance.staff_profile.save()
