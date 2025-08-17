from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Hotel, Location

@receiver(post_delete, sender=Hotel)
def delete_related_location(sender, instance, **kwargs):
    """Delete the related Location when a Hotel is deleted."""
    if instance.location:
        instance.location.delete()