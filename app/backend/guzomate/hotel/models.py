from django.db import models
import uuid
from accounts.models import User
from .utils.path import dynamic_upload_path
# Create your models here.

class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    latitude = models.DecimalField(max_digits=25, decimal_places=9, blank=False) # north +ve or south -ve
    longitude = models.DecimalField(max_digits=25, decimal_places=9, blank=False) # east +ve or west -ve
    local_name = models.CharField(max_length=30, blank=False) # local area name

    class Meta:
        unique_together = ('latitude', 'longitude')

    def __str__(self):
        return f"location_id: {self.id} - location_name: {self.local_name}"

class City(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=15, null=False, blank=False, db_index=True)
    description = models.TextField(blank=False, null=False)
    location = models.OneToOneField(Location, on_delete=models.SET_NULL, blank=False, null=True)

    def __str__(self):
        return f"city_id: {self.id} - city_name: {self.name}"

class Hotel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    owner = models.UUIDField(blank=False, null=False)
    name = models.CharField(max_length=30, blank=False, db_index=True)
    location = models.OneToOneField(Location, on_delete=models.SET_NULL, null=True, blank=False)
    star = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"hotel_id: {self.id} - hotel_name: {self.name} - star: {self.star}"

class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="rooms")
    description = models.TextField(blank=False, null=False)
    type = models.CharField(max_length=15, blank=False, null=False, db_index=True)
    room_no = models.IntegerField(blank=False, null=False)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    available = models.BooleanField(default=True, db_index=True)
    number_of_beds = models.IntegerField(blank=False, null=False)

    # class Meta:
    #     unique_together = ('hotel', 'room_no')
    def __str__(self):
        return f"room_id: {self.id} room_type: {self.type} - hotel_id: {self.hotel}"

class Amenities(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=15, blank=False, null=False, db_index=True)
    description = models.TextField(blank=False, null=False)
    availability = models.BooleanField(default=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='amenities')
    amenityable_type = models.CharField(max_length=15, default="Hotel")
    amenityable_id = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True, related_name='room_amenities')

    def __str__(self):
        return f"amenity_id: {self.id} - amenity_name: {self.name} - hotel: {self.hotel}"

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=15, blank=False, null=True, db_index=True)
    description = models.TextField(blank=False, null=False)
    accessibility = models.CharField(
                                       max_length=4, 
                                       choices=[
                                           ('Free', 'Free'),
                                            ('Paid','Paid')
                                            ], 
                                       default='Free')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="events")

class LocalAttraction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=20, blank=False, null=False, db_index=True)
    description = models.TextField(blank=False, null=False)
    accessibility = models.CharField(
                                       max_length=4, 
                                       choices=[
                                           ('Free', 'Free'),
                                            ('Paid','Paid')
                                            ], 
                                       default='Free',
                                       db_index=True
                                       )
    type = models.CharField(max_length=20, null=False, blank=False, db_index=True)
    location = models.OneToOneField(Location, on_delete=models.SET_NULL, null=True, blank=False)
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=False, null=False)
    availability = models.BooleanField(default=True)

class HotelAttraction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=False, blank=False, related_name="hotel_attractions")
    attraction = models.ForeignKey(LocalAttraction, on_delete=models.CASCADE, null=False, blank=False, related_name="attraction_hotels")
    distance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=dynamic_upload_path, null=True, blank=True)
    uploaded_at = models.DateField(auto_now_add=True)

    # Polymorphic fields
    imageable_type = models.CharField(max_length=15, blank=False, null=False)
    imageable_id = models.UUIDField(blank=False, null=False)

    # Optional hotel/city ID for querying
    hotel = models.UUIDField(blank=True, null=True, db_index=True)
    city = models.UUIDField(blank=True, null=True, db_index=True)

    # Optional names for folder structure
    hotel_name = models.CharField(max_length=15, blank=True, null=True)
    city_name = models.CharField(max_length=15, blank=True, null=True)


class HotelCities(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='hotels')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='cities')


# class HotelHistory(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     guest_name = models.CharField(max_length=255)
#     guest_contact = models.CharField(max_length=50)
#     guest_nationality = models.CharField(max_length=100)
#     guest_gender = models.CharField(
#                                      max_length=6, 
#                                      choices=[
#                                          ('Male', 'Male'),
#                                          ('Female', 'Female'),
#                                         ],
#                                       default='Male'
#                                     )
#     booking = models.ForeignKey('Booking', on_delete=models.DO_NOTHING, related_name='histories')
#     created_at = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.guest_name} - {self.booking_id}"