from django.db import models
import uuid
from accounts.models import User
# Create your models here.

class Location(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    latitude = models.DecimalField(max_digits=25, decimal_places=9, blank=False) # north +ve or south -ve
    longitude = models.DecimalField(max_digits=25, decimal_places=9, blank=False) # east +ve or west -ve
    local_name = models.CharField(max_length=30, blank=False) # local area name

    def __str__(self):
        return f"id: {self.id} - name: {self.local_name}"

class Hotel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="hotels")
    name = models.CharField(max_length=30, blank=False, db_index=True)
    location = models.OneToOneField(Location, on_delete=models.SET_NULL, null=True, blank=False, db_index=True)
    star = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
