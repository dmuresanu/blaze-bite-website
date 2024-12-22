# core/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import StaffProfile

@receiver(post_save, sender=User)
def create_staff_profile(sender, instance, created, **kwargs):
    if created:
        StaffProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_staff_profile(sender, instance, **kwargs):
    if hasattr(instance, 'staff_profile'):
        instance.staff_profile.save()
