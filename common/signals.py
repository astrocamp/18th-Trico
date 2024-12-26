from django.db.models.signals import pre_save
from django.dispatch import receiver
from services.models import Service
from users.models import Profile

@receiver(pre_save, sender=Profile)
def process_profile_image(sender, instance, **kwargs):
    if instance.photo and not getattr(instance, "_is_photo_processed", False):
        instance.process_and_upload_image(instance.photo, "profile_photos")
        instance._is_photo_processed = True

@receiver(pre_save, sender=Service)
def process_service_image(sender, instance, **kwargs):
    if instance.photo and not getattr(instance, "_is_photo_processed", False):
        instance.process_and_upload_image(instance.photo, "service_photos")
        instance._is_photo_processed = True