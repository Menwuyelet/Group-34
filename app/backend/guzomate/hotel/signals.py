from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Hotel, Location, Event, Room, Amenities, Image
from accounts.models import User
import os

@receiver(post_delete, sender=Hotel)
def delete_related_location(sender, instance, **kwargs):
    """Delete the related Location when a Hotel is deleted."""
    instance.location.delete()
    
    Room.objects.filter(hotel=instance).delete()

    # Delete hotel images
    Image.objects.filter(imageable_type="Hotel",hotel=instance.id).delete()

    # Delete hotel amenities
    Amenities.objects.filter(amenityable_type="Hotel", amenityable_id=instance.id).delete()

    # Delete events
    Event.objects.filter(hotel=instance).delete()

    #Delet users
    User.objects.filter(hotel=instance, role__in=['manager', 'reception']).delete()

@receiver(post_delete, sender=Room)
def delete_related_room_images(sender, instance, **kwargs):
    """Delete all images related to a Room when the Room is deleted."""
    Image.objects.filter(imageable_type="Room", imageable_id=instance.id).delete()
    # Delete room amenities
    Amenities.objects.filter(amenityable_type="Room", amenityable_id=instance.id).delete()


@receiver(post_delete, sender=Event)
def delete_event_images(sender, instance, **kwargs):
    """Delete all images related to an Event when the Event is deleted."""
    Image.objects.filter(imageable_type="Event", imageable_id=instance.id).delete()

@receiver(post_delete, sender=Amenities)
def delete_related_amenity_images(sender, instance, **kwargs):
    """Delete all images related to an Amenity when it is deleted."""
    Image.objects.filter(imageable_type="Amenity", imageable_id=instance.id).delete()

@receiver(post_delete, sender=Image)
def delete_image_file(sender, instance, **kwargs):
    """Delete the image file from the filesystem when the Image instance is deleted."""
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)