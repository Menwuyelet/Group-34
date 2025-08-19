import os
from django.utils import timezone

def user_image_upload_path(instance, filename):
    """
    Store user profile images in 'users/<user_id>/<uuid>.ext'
    """
    ext = filename.split('.')[-1]
    timestamp = int(timezone.now().timestamp())
    filename = f"{timestamp}.{ext}"

    return os.path.join('profile', str(instance.id), filename)




def dynamic_upload_path(instance, filename):
    """
    Dynamic path based on imageable_type:
    - Hotel-related: hotels/<hotel_name>/<model>/<instance_id>/<timestamp>.<ext>
    - City-related: cities/<city_name>/<model>/<instance_id>/<timestamp>.<ext>
    """
    ext = filename.split('.')[-1]
    timestamp = int(timezone.now().timestamp())
    filename = f"{timestamp}.{ext}"



    # Hotel-related
    if instance.imageable_type.lower() in ['hotel', 'room', 'amenity', 'event']:
        # Assume instance.hotel_name is set when creating the image
        hotel_name = getattr(instance, 'hotel_name', 'unknown_hotel').replace(' ', '_').lower()
        return os.path.join('hotels', hotel_name, instance.imageable_type.lower(), str(instance.imageable_id), filename)

    # City-related
    elif instance.imageable_type.lower() in ['city', 'localattraction']:
        # Assume instance.city_name is set when creating the image
        city_name = getattr(instance, 'city_name', 'unknown_city').replace(' ', '_').lower()
        return os.path.join('cities', city_name, instance.imageable_type.lower(), str(instance.imageable_id), filename)
    # User-related
    elif instance.imageable_type.lower() in ['city', 'localattraction']:
        # Assume instance.city_name is set when creating the image
        city_name = getattr(instance, 'city_name', 'unknown_city').replace(' ', '_').lower()
        return os.path.join('cities', city_name, instance.imageable_type.lower(), str(instance.imageable_id), filename)

    # Fallback
    return os.path.join('uploads', instance.imageable_type.lower(), str(instance.imageable_id), filename)