from django.shortcuts import render
from accounts.serializers import StaffSerializer
from accounts.models import User
from accounts.permissions import IsReceptionist, IsManagerOfHotel, IsOwnerofHotel, IsAdmin
from rest_framework import generics, viewsets
from .serializers import HotelSerializer, RoomSerializer, HotelImageSerializer
from .models import Hotel, Room, Image
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
    permission_classes = [IsManagerOfHotel | IsOwnerofHotel]

    def perform_create(self, serializer):
        hotel_id = self.kwargs.get('hotel_id')
        hotel = Hotel.objects.get(id=hotel_id)
        serializer.save(hotel=hotel)

class RoomUpdateView(generics.UpdateAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsManagerOfHotel | IsOwnerofHotel]
    lookup_field = 'id'
    lookup_url_kwarg = 'room_id' 
    def get_queryset(self):
        hotel_id = self.kwargs.get('hotel_id')
        return Room.objects.filter(hotel_id=hotel_id)

    def perform_update(self, serializer):
        serializer.save() 

class RoomDestroyView(generics.DestroyAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsManagerOfHotel | IsOwnerofHotel]
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
