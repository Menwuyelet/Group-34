from rest_framework import serializers
from .models import Review, Booking
from hotel.models import Hotel
from accounts.models import User
import re
from django.db import transaction



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


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    hotel = serializers.PrimaryKeyRelatedField(read_only=True)
    room = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'user', 'description', 'hotel', 'room', 'guest_name', 'guest_phone', 'guest_nationality', 'guest_gender', 'number_of_adults', 'number_of_children', 'start_date', 'end_date', 'total_price', 'discount', 'booking_source', 'status', 'payment', 'created_at', 'updated_at']
        read_only_fields = ['id', 'booking_source', 'status', 'payment', 'created_at',  'total_price', 'discount', 'updated_at']

    def validate_phone(self, value):
        if not re.match(r'^\+?\d{7,15}$', value):
            raise serializers.ValidationError("Invalid phone number format.")
        return value

    def validate_user(self, value):
        try:
            user = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError({"User": "the provided user does not exist."})
        return value
    
    def validate_hotel(self, value):
        try:
            hotel = Hotel.objects.get(id=value)
        except Hotel.DoesNotExist:
            raise serializers.ValidationError({"Hotel": "the hotel you entered doesn't exist."})
        return value

    def validate(self, attrs):
        no_adults = attrs.get('number_of_adults')
        no_children = attrs.get('number_of_children', 0.0)
        if no_adults < 0 or no_adults > 50:
            raise serializers.ValidationError({"Number of adults": "enter valid number of adults."})
        if no_children < 0 or no_children > 50:
            raise serializers.ValidationError({"Number of children": "enter valid number of children."})
        if no_adults == 0 and no_children == 0:
            raise serializers.ValidationError({"Number of guests": "number of guests mus be greater than zero."})

        return attrs
    

    @transaction.atomic
    def create(self, validated_data):
        start = validated_data['start_date']
        end = validated_data['end_date']
        duration = (end - start).days
        if duration <= 0:
            raise serializers.ValidationError("End date must be after start date.")

        # Base price from room
        room = validated_data['room']
        base_price = room.price_per_night * duration

        # Apply discount if any
        discount_percent = validated_data.get('discount', 0) or 0
        total_price = float(base_price) * (1 - discount_percent / 100)

        validated_data['total_price'] = total_price
        booking = Booking.objects.create(**validated_data)
        return booking
    

# class BookingStatusSerializer(serializers.ModelSerializer):
    
    # @transaction.atomic
    # def update(self, instance, validated_data):
    #     for attr, value in validated_data.item():
    #         setattr(instance, attr, value)
        
    #     instance.save()
    #     return instance




# class CityImageSerializer(serializers.ModelSerializer):
#     city = serializers.HiddenField(default=None)
#     class Meta:
#         model = Image
#         fields = ['id', 'image', 'imageable_type', 'imageable_id', 'city_name', 'uploaded_at', 'city']
#         read_only_fields = ['id', 'uploaded_at']
    
#     @transaction.atomic
#     def create(self, validated_data):
#         picture = validated_data.pop('image')
#         pic = validate_picture(picture)
#         image = Image.objects.create(image=pic, **validated_data)
#         return image
    
#     @transaction.atomic
#     def update(self, instance, validated_data):
#         if 'image' in validated_data:
#             picture = validated_data.pop('image')
#             pic = validate_picture(picture)
#             instance.image = pic

#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)

#         instance.save()
#         return instance 
    
# class CitySerializer(serializers.ModelSerializer):
#     location = LocationSerializer()
#     class Meta:
#         model = City
#         fields = ['id', 'name', 'description', 'location']
#         read_only_fields = ['id']

#     @transaction.atomic
#     def create(self, validated_data):
#         location_data = validated_data.pop('location')
#         location = Location.objects.create(**location_data)
#         city = City.objects.create(location=location, **validated_data)
#         return city

#     @transaction.atomic
#     def update(self, instance, validated_data):
#         location_data = validated_data.pop('location', None)
#         if location_data:
#             for attr, value in location_data.items():
#                 setattr(instance.location, attr, value)
#             instance.location.save()
        
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()
#         return instance

# class LocalAttractionSerializer(serializers.ModelSerializer):
#     location = LocationSerializer()
#     city = serializers.UUIDField(write_only=True)

#     class Meta:
#         model = LocalAttraction
#         fields = ['id', 'name', 'description', 'accessibility', 'type', 'location', 'city', 'availability']
#         read_only_fields = ['id']
    
#     def validate_city(self, value):
#         try:
#             city = City.objects.get(id=value)
#         except Hotel.DoesNotExist:
#             raise serializers.ValidationError({"City": "the City you entered doesn't exist."})
#         return city

#     @transaction.atomic
#     def create(self, validated_data):
#         location_data = validated_data.pop('location')
#         location = Location.objects.create(**location_data)
#         city = validated_data.pop('city')
#         attraction = LocalAttraction.objects.create(location=location, city=city, **validated_data)
#         return attraction

#     @transaction.atomic
#     def update(self, instance, validated_data):
#         location_data = validated_data.pop('location', None)
#         city = validated_data.pop('city', None)
#         if location_data:
#             for attr, value in location_data.items():
#                 setattr(instance.location, attr, value)
#             instance.location.save()
        
#         if city:
#             instance.city=city

#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()
#         return instance

# class HotelCitiesSerializers(serializers.ModelSerializer):
#     city = serializers.UUIDField(write_only=True)
#     hotel = serializers.UUIDField(write_only=True)

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
#         return hotel
    
#     @transaction.atomic
#     def create(self, validated_data):
#         city = validated_data.pop('city')
#         hotel = validated_data.pop('hotel')
#         hotelCity = HotelCities.objects.create(city=city, hotel=hotel, **validated_data)
#         return hotelCity
    
#     @transaction.atomic
#     def update(self, instance, validated_data):
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()
#         return instance