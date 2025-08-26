from rest_framework import serializers
from .models import Review, City, LocalAttraction, HotelCities
from hotel.models import Hotel, Location, Image
from hotel.serializers import LocationSerializer
from django.db import transaction
from accounts.utils.validators import validate_picture
import uuid


class ReviewSerializer(serializers.ModelSerializer):
    hotel = serializers.PrimaryKeyRelatedField(read_only=True)  # read-only now
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'hotel', 'user', 'content', 'rating', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_rating(self, value):
        if not value:
            raise serializers.ValidationError({"value": "rating value must be provided."})
        if value < 0 or value > 5:
            raise serializers.ValidationError({"value": "value must be between 0 and 5."})
        return value
    
    @transaction.atomic
    def create(self, validated_data):
        return Review.objects.create(**validated_data)
    
    @transaction.atomic
    def update(self, instance, validated_data):
        for attr, value in validated_data.item():
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

class CityImageSerializer(serializers.ModelSerializer):
    city = serializers.HiddenField(default=None)
    imageable_type = serializers.CharField(read_only=True)
    class Meta:
        model = Image
        fields = ['id', 'image', 'imageable_type', 'imageable_id', 'city_name', 'uploaded_at', 'city']
        read_only_fields = ['id', 'uploaded_at','imageable_type', 'imageable_id']
    
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

class LocalAttractionSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    city = serializers.UUIDField(read_only=True)

    class Meta:
        model = LocalAttraction
        fields = ['id', 'name', 'description', 'accessibility', 'type', 'location', 'city', 'availability']
        read_only_fields = ['id']
    
    def validate_city(self, value):
        try:
            city = City.objects.get(id=value)
        except City.DoesNotExist:
            raise serializers.ValidationError({"City": "the City you entered doesn't exist."})
        return value

    @transaction.atomic
    def create(self, validated_data):
        location_data = validated_data.pop('location')
        location = Location.objects.create(**location_data)
        city = validated_data.pop('city')
        attraction = LocalAttraction.objects.create(location=location, city=city, **validated_data)
        return attraction

    @transaction.atomic
    def update(self, instance, validated_data):
        location_data = validated_data.pop('location', None)
        city = validated_data.pop('city', None)
        if location_data:
            for attr, value in location_data.items():
                setattr(instance.location, attr, value)
            instance.location.save()
        
        if city:
            instance.city=city

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
# class HotelCitiesSerializers(serializers.ModelSerializer):
#     hotel = serializers.UUIDField(read_only=True)
#     class Meta:
#         model = HotelCities
#         fields = ['id', 'city', 'hotel']
#         read_only_fields = ['id']


#     def validate_city(self, value):
#         try:
#             city = City.objects.get(id=value)
#         except Hotel.DoesNotExist:
#             raise serializers.ValidationError({"City": "the City you entered doesn't exist."})
#         return city
    
#     def validate_hotel(self, value):
#         try:
#             hotel = Hotel.objects.get(id=value)
#         except Hotel.DoesNotExist:
#             raise serializers.ValidationError({"Hotel": "the hotel you entered doesn't exist."})
#         return value
    
#     @transaction.atomic
#     def create(self, validated_data):
#         city = validated_data.pop('city')
#         hotel_id = validated_data.pop('hotel')
#         hotel = Hotel.objects.get(id=hotel_id)
#         hotelCity = HotelCities.objects.create(city=city, hotel=hotel, **validated_data)
#         return hotelCity
    
#     @transaction.atomic
#     def update(self, instance, validated_data):
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()
#         return instance
