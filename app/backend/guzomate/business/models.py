from django.db import models
import uuid
from hotel.models import Hotel, Room, Location
from accounts.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from hotel.utils.path import user_id_image_upload_path
from datetime import datetime

# Create your models here.
class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='reviews')
    content = models.TextField(blank=False, null=False)
    rating = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(0.0),MaxValueValidator(5)])
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    #online 
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='bookings', null=True, blank=True)
    
    # in person
    guest_id_image = models.ImageField(
        upload_to=user_id_image_upload_path,
        null=True,
        blank=True
    )
    receptionist = models.UUIDField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    
    ## both
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_bookings')
    room = models.ForeignKey(Room, on_delete=models.DO_NOTHING, null=False, blank=False, related_name='room_bookings')
    guest_name = models.CharField(max_length=25, null=True, blank=True)
    guest_phone = models.CharField(max_length=15, null=True, blank=True)
    guest_nationality = models.CharField(max_length=15, default="Ethiopian")
    guest_gender = models.CharField(choices=[
                                    ("Male", "Male"),
                                    ("Female", "Female")
                                    ], 
                            default="Male"
                            )
    number_of_adults = models.IntegerField(blank=False, null=False)
    number_of_children = models.IntegerField(default=0)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    total_price = models.DecimalField(null=False, blank=False, max_digits=5, decimal_places=2)
    discount = models.DecimalField(default=0.0, max_digits=5, decimal_places=1)
    booking_source = models.CharField(choices=[
                                            ('Online', 'Online'),
                                            ('In person', 'In person')
                                        ],
                                        default='Online'
                                    )
    status = models.CharField(choices=[
                                        ('Pending', 'Pending'),
                                        ('Confirmed', 'Confirmed'),
                                        ("checked_in", "Checked In"),
                                        ('Cancelled', 'Cancelled'),
                                        ('Completed', 'Completed'),
                                    ],
                                    default='Pending',
                                    null=False, 
                                    blank=False
                            )
    payment = models.CharField(choices=[
                                        ('Pending', 'Pending'),
                                        ('Completed', 'Completed'),
                                    ],
                                    default="Pending"
                            )
    payment_method = models.CharField(choices=[
                                            ("Online", "Online"),
                                            ("Cash", "Cash"),
                                            ("Card", "Card"),
                                            ("None", "None"),
                                        ],
                                        default="None"
                                    )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return  self.id
    
## to accounts
class UserHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    booking = models.UUIDField(blank=False, null=False)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.id
    
class HotelHistoryOnline(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.UUIDField(blank=False, null=False)
    booking_id = models.UUIDField(null=False, blank=False)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.id 

## to accounts
class Favorite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    hotel = models.UUIDField(null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    created_at = models.DateField(auto_now_add=True)

class City(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=15, null=False, blank=False, db_index=True)
    description = models.TextField(blank=False, null=False)
    location = models.OneToOneField(Location, on_delete=models.SET_NULL, blank=False, null=True)

    def __str__(self):
        return f"city_id: {self.id} - city_name: {self.name}"
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

class HotelCities(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    city = models.ForeignKey('business.City', on_delete=models.CASCADE, related_name='hotels')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='cities')
