from django.db.models.signals import  post_save
from django.dispatch import receiver
from business.models import Booking, HotelHistory, UserHistory
from django.core.exceptions import ObjectDoesNotExist
@receiver(post_save, sender=Booking)
def create_booking_history(sender, instance, **kwargs):
    if instance.status in ['Cancelled', 'Completed', 'Confirmed']:
        user = instance.user if instance.user else None
        try:
            HotelHistory.objects.get(booking=instance)
        except ObjectDoesNotExist:
            HotelHistory.objects.create(
                user=user,
                hotel=instance.hotel,
                booking=instance,
                source= instance.booking_source 
            )
    if instance.booking_source == "Online" and instance.status in ['Confirmed']:
        UserHistory.objects.create(
            user=instance.user,
            booking=instance, 
        )