from rest_framework import serializers
from .models import Location, Image, City, Hotel, Room, Amenities, LocalAttraction, HotelCities, HotelAttraction, Event
from accounts.utils.validators import validate_picture
from django.db import transaction
from accounts.models import User

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
    hotel = serializers.PrimaryKeyRelatedField(read_only=True)  # read-only now

    class Meta:
        model = Image
        fields = ['id', 'image', 'imageable_type', 'imageable_id', 'hotel_name', 'uploaded_at', 'hotel']
        read_only_fields = ['id', 'uploaded_at', 'imageable_id', 'hotel']


    def validate(self, attrs):
        imageable_type = attrs.get('imageable_type')
        if imageable_type not in ['Hotel', 'Room', 'Amenity', 'Event']:
            raise serializers.ValidationError({"imageable_type": "Must be 'Hotel', 'Amenity', 'Event', or 'Room'."})
        return attrs

    def validate_hotel(self, value):
        try:
            hotel = Hotel.objects.get(id=value)
        except Hotel.DoesNotExist:
            raise serializers.ValidationError({"Hotel": "the hotel you entered doesn't exist."})
        return value

    @transaction.atomic
    def create(self, validated_data):
        picture = validated_data.pop('image')
        pic = validate_picture(picture)
        image = Image.objects.create(image=pic, **validated_data)
        return image
    
    @transaction.atomic
    def update(self, instance, validated_data):
        if 'hotel' in validated_data:
            hotel = validated_data.pop('hotel')
            
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
        read_only_fields = ['id', 'uploaded_at']
    
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
    
class HotelSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    class Meta:
        model = Hotel
        fields = ['id', 'owner', 'name', 'location', 'star']
        read_only_fields = ['id']
    
    def validate_owner(self, value):
        try:
            owner = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError({"owner": "the user you entered is not an owner or doesn't exist."})
        return value
    
    @transaction.atomic
    def create(self, validated_data):
        location_data = validated_data.pop('location')
        location = Location.objects.create(**location_data)
        hotel = Hotel.objects.create(location=location, **validated_data)
        return hotel
    
    @transaction.atomic
    def update(self, instance, validated_data):
        location_data = validated_data.pop('location', None)
        if location_data:
            for attr, value in location_data.items():
                setattr(instance.location, attr, value)
            instance.location.save()
        
        owner = validated_data.pop('owner', None)
        if owner:
            instance.owner = owner
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
class RoomSerializer(serializers.ModelSerializer):
    hotel = serializers.PrimaryKeyRelatedField(
        queryset=Hotel.objects.all(),
        required=False  
    )
    class Meta:
        model = Room
        fields = ['id', 'hotel', 'description', 'type', 'room_no', 'price_per_night', 'available', 'number_of_beds']
        read_only_fields = ['id']

    def validate_hotel(self, value):
        try:
            hotel = Hotel.objects.get(id=value)
        except Hotel.DoesNotExist:
            raise serializers.ValidationError({"Hotel": "the hotel you entered doesn't exist."})
        return value
    
    @transaction.atomic
    def create(self, validated_data):
        return Room.objects.create(**validated_data)
   
    @transaction.atomic
    def update(self, instance, validated_data):
        if 'hotel' in validated_data:
            hotel = validated_data.pop('hotel')
            
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class HotelAmenitiesSerializer(serializers.ModelSerializer):
    hotel = serializers.UUIDField(write_only=True)
    model = Amenities
    class Meta:
        fields = ['id', 'name', 'description', 'available', 'hotel', 'amenityable_type']
        read_only_fields = ['id']

    def validate_hotel(self, value):
        try:
            hotel = Hotel.objects.get(id=value)
        except Hotel.DoesNotExist:
            raise serializers.ValidationError({"Hotel": "the hotel you entered doesn't exist."})
        return hotel
    
    @transaction.atomic
    def create(self, validated_data):
        hotel = validated_data.pop('hotel')
        return Room.objects.create(hotel=hotel, **validated_data)
   
    @transaction.atomic
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
class RoomAmenitiesSerializer(serializers.ModelSerializer):
    hotel = serializers.UUIDField(write_only=True)
    room = serializers.UUIDField(write_only=True)
    class Meta:
        model = Amenities
        fields = ['id', 'name', 'description', 'available', 'hotel', 'amenityable_type', 'amenityable_id']
        read_only_fields = ['id']
   
    def validate_hotel(self, value):
        try:
            hotel = Hotel.objects.get(id=value)
        except Hotel.DoesNotExist:
            raise serializers.ValidationError({"Hotel": "the hotel you entered doesn't exist."})
        return hotel
    
    def validate_room(self, value):
        try:
            room = Room.objects.get(id=value)
        except Room.DoesNotExist:
            raise serializers.ValidationError({"Room": "the selected room doesn't exist."})
        return room
    
    @transaction.atomic
    def create(self, validated_data):
        hotel = validated_data.pop('hotel')
        room = validated_data.pop('room')
        return Room.objects.create(hotel=hotel, room=room, **validated_data)
   
    @transaction.atomic
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    
class EventSerializer(serializers.ModelSerializer):
    hotel = serializers.UUIDField(write_only=True)

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'accessibility', 'price', 'hotel']
        read_only_fields = ['id']

    def validate_hotel(self, value):
        try:
            hotel = Hotel.objects.get(id=value)
        except Hotel.DoesNotExist:
            raise serializers.ValidationError({"Hotel": "the hotel you entered doesn't exist."})
        return hotel
    @transaction.atomic
    def create(self, validated_data):
        hotel = validated_data.pop('hotel')
        event = Event.objects.create(hotel=hotel, **validated_data)
        return event
    
    @transaction.atomic
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    

class LocalAttractionSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    city = serializers.UUIDField(write_only=True)

    class Meta:
        model = LocalAttraction
        fields = ['id', 'name', 'description', 'accessibility', 'type', 'location', 'city', 'availability']
        read_only_fields = ['id']
    
    def validate_city(self, value):
        try:
            city = City.objects.get(id=value)
        except Hotel.DoesNotExist:
            raise serializers.ValidationError({"City": "the City you entered doesn't exist."})
        return city

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

class HotelAttractionSerializer(serializers.ModelSerializer):
    hotel = serializers.UUIDField(write_only=True)
    attraction = serializers.UUIDField(write_only=True)

    class Meta:
        model = HotelAttraction
        fields = ['id', 'hotel', 'attraction', 'distance']
        read_only_field = ['id', 'distance']

    def validate_hotel(self, value):
        try:
            hotel = Hotel.objects.get(id=value)
        except Hotel.DoesNotExist:
            raise serializers.ValidationError({"Hotel": "the hotel you entered doesn't exist."})
        return hotel

    def validate_attraction(self, value):
        try: 
            attraction = LocalAttraction.objects.get(id=value)
        except LocalAttraction.DoesNotExist:
             raise serializers.ValidationError({"Attraction": "the attraction you entered doesn't exist."})
        return attraction
    
    @transaction.atomic
    def create(self, validated_data):
        hotel = validated_data.pop('hotel')
        attraction = validated_data.pop('attraction')
        hotelAttraction = HotelAttraction.objects.create(hotel=hotel, attraction=attraction, **validated_data)
        return hotelAttraction
    
    @transaction.atomic
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
class HotelCitiesSerializers(serializers.ModelSerializer):
    city = serializers.UUIDField(write_only=True)
    hotel = serializers.UUIDField(write_only=True)

    class Meta:
        model = HotelCities
        fields = ['id', 'city', 'hotel']
        read_only_fields = ['id']


    def validate_city(self, value):
        try:
            city = City.objects.get(id=value)
        except Hotel.DoesNotExist:
            raise serializers.ValidationError({"City": "the City you entered doesn't exist."})
        return city
    
    def validate_hotel(self, value):
        try:
            hotel = Hotel.objects.get(id=value)
        except Hotel.DoesNotExist:
            raise serializers.ValidationError({"Hotel": "the hotel you entered doesn't exist."})
        return hotel
    
    @transaction.atomic
    def create(self, validated_data):
        city = validated_data.pop('city')
        hotel = validated_data.pop('hotel')
        hotelCity = HotelCities.objects.create(city=city, hotel=hotel, **validated_data)
        return hotelCity
    
    @transaction.atomic
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    