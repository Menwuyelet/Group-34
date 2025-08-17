from django.shortcuts import render
from accounts.serializers import StaffSerializer
from accounts.models import User
from accounts.permissions import IsReceptionist, IsManagerOfHotel, IsOwnerofHotel, IsAdmin
from rest_framework import generics, viewsets
from .serializers import HotelSerializer, RoomSerializer, HotelImageSerializer, EventSerializer, HotelAmenitiesSerializer, RoomAmenitiesSerializer, CitySerializer
from .models import Hotel, Room, Image, Event, Amenities, City
from rest_framework.permissions import AllowAny
from rest_framework import serializers
# Create your views here.

## Hotel
class HotelCreateView(generics.CreateAPIView):
    serializer_class = HotelSerializer
    permission_classes = [IsAdmin]

    def perform_create(self, serializer):
        serializer.save()
      
class HotelUpdateView(generics.UpdateAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'pk'
    lookup_url_kwarg = 'hotel_id' 
    
    def perform_update(self, serializer):
        serializer.save()

class HotelDestroyView(generics.DestroyAPIView):
    serializer_class = HotelSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'pk'
    lookup_url_kwarg = 'hotel_id' 
    queryset = Hotel.objects.all()
    
    def perform_destroy(self, instance):
        instance.delete()

class HotelViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'id'
    lookup_url_kwarg = 'hotel_id' 
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [AllowAny]
    
## Room
class RoomCreateView(generics.CreateAPIView):
    serializer_class = RoomSerializer
    # permission_classes = [IsOwnerofHotel | IsManagerOfHotel]
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        hotel_id = self.kwargs.get('hotel_id')
        hotel = Hotel.objects.get(id=hotel_id)
        serializer.save(hotel=hotel)

class RoomUpdateView(generics.UpdateAPIView):
    serializer_class = RoomSerializer
    # permission_classes = [IsOwnerofHotel | IsManagerOfHotel]
    permission_classes = [AllowAny]
    lookup_field = 'id'
    lookup_url_kwarg = 'room_id' 
    def get_queryset(self):
        hotel_id = self.kwargs.get('hotel_id')
        return Room.objects.filter(hotel_id=hotel_id)

    def perform_update(self, serializer):
        serializer.save() 

class RoomDestroyView(generics.DestroyAPIView):
    serializer_class = RoomSerializer
    # permission_classes = [IsOwnerofHotel | IsManagerOfHotel]
    permission_classes = [AllowAny]
    lookup_url_kwarg = 'room_id' 
    def get_queryset(self):
        hotel_id = self.kwargs.get('hotel_id')
        return Room.objects.filter(hotel_id=hotel_id)

class RoomViewSets(viewsets.ReadOnlyModelViewSet):
    serializer_class = RoomSerializer
    permission_classes = [AllowAny]
    lookup_url_kwarg = 'room_id' 

    def get_queryset(self):
        hotel_id = self.kwargs.get('hotel_id')  
        return Room.objects.filter(hotel_id=hotel_id)

## Event

class EventCreateView(generics.CreateAPIView):
    serializer_class = EventSerializer
    # permission_classes = [IsOwnerofHotel | IsManagerOfHotel]
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        hotel_id = self.kwargs.get('hotel_id')
        hotel = Hotel.objects.get(id=hotel_id)
        serializer.save(hotel=hotel)

class EventUpdateView(generics.UpdateAPIView):
    serializer_class = EventSerializer
    # permission_classes = [IsOwnerofHotel | IsManagerOfHotel]
    permission_classes = [AllowAny]
    lookup_field = 'id'
    lookup_url_kwarg = 'event_id'

    def get_queryset(self):
        hotel_id = self.kwargs.get('hotel_id')
        return Event.objects.filter(hotel_id=hotel_id)

    def perform_update(self, serializer):
        serializer.save()

class EventDestroyView(generics.DestroyAPIView):
    serializer_class = EventSerializer
    # permission_classes = [IsOwnerofHotel | IsManagerOfHotel]
    permission_classes = [AllowAny]
    lookup_url_kwarg = 'event_id'

    def get_queryset(self):
        hotel_id = self.kwargs.get('hotel_id')
        return Event.objects.filter(hotel_id=hotel_id)

class EventViewSets(viewsets.ReadOnlyModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [AllowAny]
    lookup_url_kwarg = 'event_id'

    def get_queryset(self):
        hotel_id = self.kwargs.get('hotel_id')
        return Event.objects.filter(hotel_id=hotel_id)

## Hotel Amenities

class AmenityCreateView(generics.CreateAPIView):
    serializer_class = HotelAmenitiesSerializer
    # permission_classes = [IsOwnerofHotel | IsManagerOfHotel]
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        hotel_id = self.kwargs.get('hotel_id')
        hotel = Hotel.objects.get(id=hotel_id)
        serializer.save(hotel=hotel, amenityable_type="Hotel")

class AmenityUpdateView(generics.UpdateAPIView):
    serializer_class = HotelAmenitiesSerializer
    # permission_classes = [IsOwnerofHotel | IsManagerOfHotel]
    permission_classes = [AllowAny]
    lookup_field = 'id'
    lookup_url_kwarg = 'amenity_id'

    def get_queryset(self):
        hotel_id = self.kwargs.get('hotel_id')
        return Amenities.objects.filter(hotel_id=hotel_id, amenityable_type="Hotel")

    def perform_update(self, serializer):
        serializer.save()

class AmenityDestroyView(generics.DestroyAPIView):
    serializer_class = HotelAmenitiesSerializer
    # permission_classes = [IsOwnerofHotel | IsManagerOfHotel]
    permission_classes = [AllowAny]
    lookup_url_kwarg = 'amenity_id'

    def get_queryset(self):
        hotel_id = self.kwargs.get('hotel_id')
        return Amenities.objects.filter(hotel_id=hotel_id, amenityable_type="Hotel")

class AmenityViewSets(viewsets.ReadOnlyModelViewSet):
    serializer_class = HotelAmenitiesSerializer
    permission_classes = [AllowAny]
    lookup_url_kwarg = 'amenity_id'

    def get_queryset(self):
        hotel_id = self.kwargs.get('hotel_id')
        amenityable_type="Hotel"
        return Amenities.objects.filter(hotel_id=hotel_id, amenityable_type="Hotel")

## Room Amenities

class RoomAmenityCreateView(generics.CreateAPIView):
    serializer_class = RoomAmenitiesSerializer
    # permission_classes = [IsOwnerofHotel | IsManagerOfHotel]
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        hotel_id = self.kwargs.get('hotel_id')
        room_id = self.kwargs.get('room_id')
        hotel = Hotel.objects.get(id=hotel_id)
        room = Room.objects.get(id=room_id, hotel_id=hotel_id)
        serializer.save(hotel=hotel, amenityable_id=room,  amenityable_type="Room" )

class RoomAmenityUpdateView(generics.UpdateAPIView):
    serializer_class = RoomAmenitiesSerializer
    # permission_classes = [IsOwnerofHotel | IsManagerOfHotel]
    permission_classes = [AllowAny]
    lookup_field = 'id'
    lookup_url_kwarg = 'amenity_id'

    def get_queryset(self):
        hotel_id = self.kwargs.get('hotel_id')
        room_id = self.kwargs.get('room_id')
        return Amenities.objects.filter(hotel_id=hotel_id, amenityable_id=room_id)

    def perform_update(self, serializer):
        serializer.save()

class RoomAmenityDestroyView(generics.DestroyAPIView):
    serializer_class = RoomAmenitiesSerializer
    # permission_classes = [IsOwnerofHotel | IsManagerOfHotel]
    permission_classes = [AllowAny]
    lookup_url_kwarg = 'amenity_id'

    def get_queryset(self):
        hotel_id = self.kwargs.get('hotel_id')
        room_id = self.kwargs.get('room_id')
        return Amenities.objects.filter(hotel_id=hotel_id, amenityable_id=room_id)

class RoomAmenityViewSets(viewsets.ReadOnlyModelViewSet):
    serializer_class = RoomAmenitiesSerializer
    permission_classes = [AllowAny]
    lookup_url_kwarg = 'amenity_id'

    def get_queryset(self):
        hotel_id = self.kwargs.get('hotel_id')
        room_id = self.kwargs.get('room_id')
        return Amenities.objects.filter(hotel_id=hotel_id, amenityable_id=room_id)

## HotelImage

class HotelImageCreateView(generics.CreateAPIView):
    serializer_class = HotelImageSerializer
    permission_classes = [IsManagerOfHotel | IsOwnerofHotel]
    # permission_classes = [AllowAny]

    def perform_create(self, serializer):
        imageable_type = self.request.data.get('imageable_type')
        if imageable_type == 'Hotel':
            hotel_id = self.kwargs.get('hotel_id')
            hotel = Hotel.objects.get(id=hotel_id)
            serializer.save(
                imageable_id=hotel.id,
                hotel=hotel.id,
                hotel_name=hotel.name
            )
        elif imageable_type == 'Room':
            room_id = self.kwargs.get('room_id')
            room = Room.objects.get(id=room_id)
            serializer.save(
                imageable_id=room.id,
                hotel=room.hotel.id,
                hotel_name=room.hotel.name
            )
        else:
            raise serializers.ValidationError({"imageable_type": "Invalid type"})

class HotelImageUpdateView(generics.UpdateAPIView):
    serializer_class = HotelImageSerializer
    permission_classes = [IsManagerOfHotel | IsOwnerofHotel]
    # permission_classes = [AllowAny]
    lookup_field = 'id' 
    lookup_url_kwarg = 'image_id'

    def get_queryset(self):
        hotel_id = self.kwargs.get('hotel_id')
        return Image.objects.filter(hotel=hotel_id)

    def perform_update(self, serializer):
        serializer.save() 

class HotelImageDestroyView(generics.DestroyAPIView):
    serializer_class = HotelImageSerializer
    permission_classes = [IsManagerOfHotel | IsOwnerofHotel]
    # permission_classes = [AllowAny]
    lookup_field = 'id'
    lookup_url_kwarg = 'image_id'

    def get_queryset(self):
        hotel_id = self.kwargs.get('hotel_id')
        return Image.objects.filter(hotel=hotel_id)
    
class HotelImageViewSets(viewsets.ReadOnlyModelViewSet):
    serializer_class = HotelImageSerializer
    permission_classes = [AllowAny]
    lookup_url_kwarg = 'image_id' 
    def get_queryset(self):
        hotel_id = self.kwargs.get('hotel_id')  
        return Image.objects.filter(hotel=hotel_id, imageable_type='Hotel')

## Room image views

class RoomImageListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = HotelImageSerializer

    def get_queryset(self):
        hotel_id = self.kwargs['hotel_id']
        room_id = self.kwargs['room_id']
        return Image.objects.filter(hotel=hotel_id, imageable_id=room_id)

class RoomImageDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = HotelImageSerializer
    lookup_url_kwarg = "image_id"

    def get_queryset(self):
        hotel_id = self.kwargs['hotel_id']
        room_id = self.kwargs['room_id']
        return Image.objects.filter(hotel=hotel_id, imageable_id=room_id)

class RoomImageCreateView(generics.CreateAPIView):
    # permission_classes = [AllowAny]
    permission_classes = [IsOwnerofHotel | IsManagerOfHotel]
    serializer_class = HotelImageSerializer

    def perform_create(self, serializer):
        hotel_id = self.kwargs['hotel_id']
        room_id = self.kwargs['room_id']
        hotel = Hotel.objects.get(id=hotel_id)
        serializer.save(imageable_type='Room', imageable_id=room_id, hotel=hotel_id, hotel_name=hotel.name)

class RoomImageUpdateView(generics.UpdateAPIView):
    # permission_classes = [AllowAny]
    permission_classes = [IsOwnerofHotel | IsManagerOfHotel]
    serializer_class = HotelImageSerializer
    lookup_url_kwarg = "image_id"

    def get_queryset(self):
        hotel_id = self.kwargs['hotel_id']
        room_id = self.kwargs['room_id']
        return Image.objects.filter(hotel=hotel_id, imageable_id=room_id)

class RoomImageDestroyView(generics.DestroyAPIView):
    # permission_classes = [AllowAny]
    permission_classes = [IsOwnerofHotel | IsManagerOfHotel]
    serializer_class = HotelImageSerializer
    lookup_url_kwarg = "image_id"

    def get_queryset(self):
        hotel_id = self.kwargs['hotel_id']
        room_id = self.kwargs['room_id']
        return Image.objects.filter(hotel=hotel_id, imageable_id=room_id)
    
## Event image views

class EventImageListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = HotelImageSerializer

    def get_queryset(self):
        hotel_id = self.kwargs['hotel_id']
        event_id = self.kwargs['event_id']
        hotel = Hotel.objects.get(id=hotel_id)
        return Image.objects.filter(imageable_type='Event', imageable_id=event_id, hotel=hotel_id, hotel_name=hotel.name)

class EventImageDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = HotelImageSerializer
    lookup_url_kwarg = "image_id"

    def get_queryset(self):
        hotel_id = self.kwargs['hotel_id']
        event_id = self.kwargs['event_id']
        return Image.objects.filter(hotel=hotel_id, imageable_id=event_id, imageable_type='Event')

class EventImageCreateView(generics.CreateAPIView):
    # permission_classes = [AllowAny]
    permission_classes = [IsOwnerofHotel | IsManagerOfHotel]
    serializer_class = HotelImageSerializer

    def perform_create(self, serializer):
        hotel_id = self.kwargs['hotel_id']
        event_id = self.kwargs['event_id']
        hotel = Hotel.objects.get(id=hotel_id)
        event = Event.objects.get(id=event_id, hotel_id=hotel_id)  # ensures event belongs to hotel
        serializer.save(
            imageable_type='Event',
            imageable_id=event.id,
            hotel=hotel_id,
            hotel_name=hotel.name
        )

class EventImageUpdateView(generics.UpdateAPIView):
    # permission_classes = [AllowAny]
    permission_classes = [IsOwnerofHotel | IsManagerOfHotel]
    serializer_class = HotelImageSerializer
    lookup_url_kwarg = "image_id"

    def get_queryset(self):
        hotel_id = self.kwargs['hotel_id']
        event_id = self.kwargs['event_id']
        return Image.objects.filter(hotel=hotel_id, imageable_id=event_id, imageable_type='Event')

class EventImageDestroyView(generics.DestroyAPIView):
    # permission_classes = [AllowAny]
    permission_classes = [IsOwnerofHotel | IsManagerOfHotel]
    serializer_class = HotelImageSerializer
    lookup_url_kwarg = "image_id"

    def get_queryset(self):
        hotel_id = self.kwargs['hotel_id']
        event_id = self.kwargs['event_id']
        return Image.objects.filter(hotel=hotel_id, imageable_id=event_id, imageable_type='Event')

## City

# class CityCreateView(generics.CreateAPIView):
#     serializer_class = CitySerializer
#     permission_classes = [IsAdmin] # change to custom permission if needed

#     def perform_create(self, serializer):
#         serializer.save()

# class CityUpdateView(generics.UpdateAPIView):
#     serializer_class = CitySerializer
#     permission_classes = [IsAdmin]
#     lookup_field = 'id'
#     lookup_url_kwarg = 'city_id'

#     def get_queryset(self):
#         return City.objects.all()

#     def perform_update(self, serializer):
#         serializer.save()

# class CityDestroyView(generics.DestroyAPIView):
#     serializer_class = CitySerializer
#     permission_classes = [IsAdmin]
#     lookup_field = 'id'
#     lookup_url_kwarg = 'city_id'

#     def get_queryset(self):
#         return City.objects.all()

# class CityListView(generics.ListAPIView):
#     serializer_class = CitySerializer
#     permission_classes = [AllowAny]

#     def get_queryset(self):
#         return City.objects.all()

# class CityDetailView(generics.RetrieveAPIView):
#     serializer_class = CitySerializer
#     permission_classes = [AllowAny]
#     lookup_field = 'id'
#     lookup_url_kwarg = 'city_id'

#     def get_queryset(self):
#         return City.objects.all()

# class CityViewSets(viewsets.ReadOnlyModelViewSet):
#     serializer_class = CitySerializer
#     permission_classes = [AllowAny]
#     lookup_url_kwarg = 'city_id'

#     def get_queryset(self):
#         return City.objects.all()
