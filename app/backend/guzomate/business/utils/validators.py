from business.models import Booking

def is_room_available(room, start_date, end_date, exclude_booking=None):
    overlapping_bookings = Booking.objects.filter(
        room=room,
        start_date__lt=end_date,   
        end_date__gt=start_date,
        status__in=["Confirmed", "Checked_in"]
    )
    if exclude_booking:
        overlapping_bookings = overlapping_bookings.exclude(id=exclude_booking.id)
    return not overlapping_bookings.exists()