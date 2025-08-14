from rest_framework import serializers
from .models import Location, Image, City, Hotel, Room, Amenities, LocalAttraction, HotelCities, HotelAttraction, Event
from accounts.utils.validators import validate_picture
from django.db import transaction

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'latitude', 'longitude', 'local_name']
        read_only_fields = ['id']

    def validate(self, attrs):
        latitude = attrs.get('latitude')
        if latitude is not None:
            if not (-90 <= latitude <= 90):
                raise serializers.ValidationError({"latitude": "Latitude must be between -90 and 90."})

        longitude = attrs.get('longitude')
        if longitude is not None:
            if not (-180 <= longitude <= 180):
                raise serializers.ValidationError({"longitude": "Longitude must be between -180 and 180."})

        return attrs
    
    @transaction.atomic
    def create(self, validated_data):
        local_name = validated_data.pop('local_name', None)
        if not local_name:
            raise ValueError({"local_name": "Local name should be provided."})
    
        location = Location.objects.create(local_name=local_name, **validated_data)
        return location
    
    @transaction.atomic
    def update(self, instance, validated_data):
        local_name = validated_data.get('local_name', instance.local_name)
        if not local_name:
            raise ValueError({"local_name": "Local name should be provided."})
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

class HotelImageSerializer(serializers.ModelSerializer):
    hotel = serializers.HiddenField(default=None)
    class Meta:
        model = Image
        fields = ['id', 'image', 'imageable_type', 'imageable_id', 'hotel_name', 'uploaded_at', 'hotel']
        read_only_field = ['id', 'uploaded_at']
    
    @transaction.atomic
    def create(self, validated_data):
        picture = validated_data.pop('image')
        pic = validate_picture(picture)
        image = Image.objects.create(image=pic, **validated_data)
        return image
    
    @transaction.atomic
    def update(self, instance, validated_data):
        if 'image' in validated_data:
            picture = validated_data.pop('image')
            pic = validate_picture(picture)
            instance.image = pic

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
    
class CityImageSerializer(serializers.ModelSerializer):
    city = serializers.HiddenField(default=None)
    class Meta:
        model = Image
        fields = ['id', 'image', 'imageable_type', 'imageable_id', 'city_name', 'uploaded_at', 'city']
        read_only_field = ['id', 'uploaded_at']
    
    @transaction.atomic
    def create(self, validated_data):
        picture = validated_data.pop('image')
        pic = validate_picture(picture)
        image = Image.objects.create(image=pic, **validated_data)
        return image
    
    @transaction.atomic5
    def update(self, instance, validated_data):
        if 'image' in validated_data:
            picture = validated_data.pop('image')
            pic = validate_picture(picture)
            instance.image = pic

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance 
    
class CitySerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    class Meta:
        model = City
        fields = ['id', 'name', 'description', 'location']
        read_only_fields = ['id']

    @transaction.atomic
    def create(self, validated_data):
        location_data = validated_data.pop('location')
        location = Location.objects.create(**location_data)
        city = City.objects.create(location=location, **validated_data)
        return city

    @transaction.atomic
    def update(self, instance, validated_data):
        location_data = validated_data.pop('location', None)
        if location_data:
            for attr, value in location_data.items():
                setattr(instance.location, attr, value)
            instance.location.save()
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance