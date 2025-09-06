from rest_framework import serializers
from .models import Review, City, LocalAttraction, HotelCities, Favorite, Booking, HotelHistory, UserHistory
from hotel.models import Hotel, Location, Image
from hotel.serializers import LocationSerializer
from django.db import transaction
from accounts.utils.validators import validate_picture
from accounts.models import User
import re
from .utils.validators import is_room_available




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
    
class HotelCitiesSerializers(serializers.ModelSerializer):
    class Meta:
        model = HotelCities
        exclude = ["hotel"]
        read_only_fields = ['id']


    def validate_city(self, value):
        try:
            city = City.objects.get(id=value.id)
        except Hotel.DoesNotExist:
            raise serializers.ValidationError({"City": "the City you entered doesn't exist."})
        return city
    
    def validate_hotel(self, value):
        try:
            hotel = Hotel.objects.get(id=value)
        except Hotel.DoesNotExist:
            raise serializers.ValidationError({"Hotel": "the hotel you entered doesn't exist."})
        return value
    
    @transaction.atomic
    def create(self, validated_data):
        city = validated_data.pop('city')
        hotel_id = validated_data.pop('hotel')
        hotel = Hotel.objects.get(id=hotel_id)
        hotelCity = HotelCities.objects.create(city=city, hotel=hotel, **validated_data)
        return hotelCity
    
    @transaction.atomic
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class FavoriteSerializer(serializers.ModelSerializer):
    hotel = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Favorite
        exclude = ['user']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        favorite = Favorite.objects.create(**validated_data)
        return favorite
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

## Booking

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    hotel = serializers.PrimaryKeyRelatedField(read_only=True)
    room = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'user', 'description', 'hotel', 'room', 'guest_name', 'guest_phone', 'guest_nationality', 'guest_gender', 'number_of_adults', 'number_of_children', 'start_date', 'end_date', 'total_price', 'discount', 'booking_source', 'status', 'payment', 'created_at', 'updated_at']
        read_only_fields = ['id', 'booking_source', 'status', 'payment', 'created_at',  'total_price', 'discount', 'updated_at']

    def validate_guest_phone(self, value):
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
        no_children = attrs.get('number_of_children')
        if no_adults is not None:
            if no_adults < 0 or no_adults > 50:
                raise serializers.ValidationError({"Number of adults": "enter valid number of adults."})
        if no_children is not None:
            if no_children < 0 or no_children > 50:
                raise serializers.ValidationError({"Number of children": "enter valid number of children."})
        if no_adults is not None or no_children is not None:
            if no_adults == 0 and no_children == 0:
                raise serializers.ValidationError({"Number of guests": "number of guests must be greater than zero."})

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

        if not is_room_available(room, start, end):
            raise serializers.ValidationError({"Room": "the selected room is not available."})

        # Apply discount if any
        discount_percent = validated_data.get('discount', 0)
        total_price = float(base_price) * (1 - discount_percent / 100)

        phone = validated_data.pop('guest_phone', None)
        guest_name = validated_data.pop('guest_name', None)
        nationality = validated_data.pop('guest_nationality', None)
        gender = validated_data.pop('guest_gender', None)
        if not phone:
            user = validated_data['user']
            validated_data['guest_phone'] = user.phone
        else:
            validated_data['guest_phone'] = phone
        
        if not guest_name:
            user= validated_data['user']
            validated_data['guest_name'] = f"{user.first_name} {user.last_name}"
        else:
            validated_data['guest_name'] = guest_name
        
        if not gender:
            user = validated_data['user']
            validated_data['guest_gender'] = user.gender
        else:
            validated_data['guest_gender'] = gender
        
        if not nationality:
            user = validated_data['user']
            validated_data['guest_nationality'] = user.nationality
        else:
            validated_data['guest_nationality'] = nationality
        validated_data['total_price'] = total_price

        booking = Booking.objects.create(**validated_data)
        return booking
    
    @transaction.atomic
    def update(self, instance, validated_data):
        # Validate dates
        start = validated_data.get('start_date', instance.start_date)
        end = validated_data.get('end_date', instance.end_date)
        duration = (end - start).days
        if duration <= 0:
            raise serializers.ValidationError("End date must be after start date.")

        # Base price from room
        room = validated_data.get('room', instance.room)
        base_price = room.price_per_night * duration

        # Check room availability
        if not is_room_available(room, start, end, exclude_booking=instance):
            # exclude_booking ensures current booking dates don't block itself
            raise serializers.ValidationError({"Room": "the selected room is not available."})

        # Apply discount if any
        discount_percent = validated_data.get('discount', instance.discount) or 0
        total_price = float(base_price) * (1 - discount_percent / 100)

        # Handle guest info
        phone = validated_data.pop('guest_phone', getattr(instance, 'guest_phone', None))
        guest_name = validated_data.pop('guest_name', getattr(instance, 'guest_name', None))
        nationality = validated_data.pop('guest_nationality',getattr(instance, 'guest_nationality', None))
        gender = validated_data.pop('guest_gender', getattr(instance, 'guest_gender', None))

        if not phone:
            user = validated_data.get('user', instance.user)
            validated_data['guest_phone'] = user.phone
        else:
            validated_data['guest_phone'] = phone

        if not guest_name:
            user = validated_data.get('user', instance.user)
            validated_data['guest_name'] = f"{user.first_name} {user.last_name}"
        else:
            validated_data['guest_name'] = guest_name

        if not nationality:
            user = validated_data.get('user', instance.user)
            validated_data['guest_nationality'] = user.nationality
        else:
            validated_data['guest_nationality'] = nationality

        if not gender:
            user = validated_data.get('user', instance.user)
            validated_data['guest_gender'] = user.gender
        else:
            validated_data['guest_gender'] = gender
        validated_data['total_price'] = total_price

        # Update instance fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

class InPersonBookingSerializer(serializers.ModelSerializer):
    receptionist = serializers.PrimaryKeyRelatedField(read_only=True)
    hotel = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'user', 'receptionist', 'description', 'hotel', 'room', 'guest_name', 'guest_phone', 'guest_nationality', 'guest_gender', 'number_of_adults', 'number_of_children', 'start_date', 'end_date', 'total_price', 'discount', 'booking_source', 'status', 'payment', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'receptionist', 'booking_source', 'status',  'created_at',  'total_price', 'discount', 'updated_at']

    def validate_guest_phone(self, value):
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
        no_children = attrs.get('number_of_children')
        if no_adults is not None:
            if no_adults < 0 or no_adults > 50:
                raise serializers.ValidationError({"Number of adults": "enter valid number of adults."})
        if no_children is not None:
            if no_children < 0 or no_children > 50:
                raise serializers.ValidationError({"Number of children": "enter valid number of children."})
        if no_adults is not None or no_children is not None:
            if no_adults == 0 and no_children == 0:
                raise serializers.ValidationError({"Number of guests": "number of guests must be greater than zero."})

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        start = validated_data['start_date']
        end = validated_data['end_date']
        duration = (end - start).days
        if duration <= 0:
            raise serializers.ValidationError("End date must be after start date.")

        room = validated_data['room']
        if not is_room_available(room, start, end):
            raise serializers.ValidationError({"Room": "the selected room is not available."})

        # Apply discount if any
        base_price = room.price_per_night * duration
        discount_percent = validated_data.get('discount', 0) or 0
        total_price = float(base_price) * (1 - discount_percent / 100)
        validated_data['total_price'] = total_price

        booking = Booking.objects.create(**validated_data)
        return booking
    
    @transaction.atomic
    def update(self, instance, validated_data):
        start = validated_data.get('start_date', instance.start_date)
        end = validated_data.get('end_date', instance.end_date)
        duration = (end - start).days
        if duration <= 0:
            raise serializers.ValidationError("End date must be after start date.")

        room = validated_data.get('room', instance.room)
        base_price = room.price_per_night * duration

        if not is_room_available(room, start, end, exclude_booking=instance):
            raise serializers.ValidationError({"Room": "the selected room is not available."})

        discount_percent = validated_data.get('discount', instance.discount) or 0
        total_price = float(base_price) * (1 - discount_percent / 100)

        phone = validated_data.pop('guest_phone', getattr(instance, 'guest_phone', None))
        guest_name = validated_data.pop('guest_name', getattr(instance, 'guest_name', None))

        if not phone:
            user = validated_data.get('user', instance.user)
            validated_data['guest_phone'] = user.phone
        else:
            validated_data['guest_phone'] = phone

        if not guest_name:
            user = validated_data.get('user', instance.user)
            validated_data['guest_name'] = f"{user.first_name} {user.last_name}"
        else:
            validated_data['guest_name'] = guest_name

        validated_data['total_price'] = total_price

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
    
class BookingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['status']

    @transaction.atomic
    def update(self, instance, validated_data):
        if instance.status == 'Completed' or instance.status == 'Cancelled':
            raise serializers.ValidationError({"Booking": "the status for this booking can't be updated."})
        if validated_data['status'] == 'Pending':
            raise serializers.ValidationError({"Status": "the status can not be changed to pending."})
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
    
## Hotel History

class HotelHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelHistory
        fields = ['id', 'user', 'hotel', 'booking', 'created_at']

    
class UserHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserHistory
        fields = ['id', 'user', 'booking', 'created_at']