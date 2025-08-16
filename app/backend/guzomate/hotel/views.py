from django.shortcuts import render
from accounts.serializers import StaffSerializer
from accounts.models import User
from accounts.permissions import IsReceptionist, IsManagerOfHotel, IsOwnerofHotel, IsAdmin
from rest_framework import generics, viewsets
from .serializers import HotelSerializer, RoomSerializer, HotelImageSerializer
from .models import Hotel, Room, Image
from rest_framework.permissions import AllowAny
# Create your views here.

## Hotel
class HotelCreateView(generics.CreateAPIView):
    serializer_class = HotelSerializer
    permission_classes = [IsAdmin]

    def perform_create(self, serializer):
        serializer.save()
      
class HotelUpdateView(generics.UpdateAPIView):
    serializer_class = HotelSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'pk'
    
    def perform_update(self, serializer):
        serializer.save()

class HotelDestroyView(generics.DestroyAPIView):
    serializer_class = HotelSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        instance.delete()

class HotelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [AllowAny]
    
## Room
class RoomCreateView(generics.CreateAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsManagerOfHotel | IsOwnerofHotel]

    def perform_create(self, serializer):
        hotel = self.kwargs.get('hotel_id')
        serializer.save(hotel=hotel)

class RoomUpdateView(generics.UpdateAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsManagerOfHotel | IsOwnerofHotel]

    def get_queryset(self):
        hotel_id = self.kwargs.get('hotel_id')
        return Room.objects.filter(hotel_id=hotel_id)

    def perform_update(self, serializer):
        serializer.save() 

class RoomDestroyView(generics.DestroyAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsManagerOfHotel | IsOwnerofHotel]

    def get_queryset(self):
        hotel_id = self.kwargs.get('hotel_id')
        return Room.objects.filter(hotel_id=hotel_id)

class RoomViewSets(viewsets.ReadOnlyModelViewSet):
    serializer_class = RoomSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        hotel_id = self.kwargs.get('hotel_id')  
        return Room.objects.filter(hotel_id=hotel_id)

## HotelImage

class HotelImageCreateView(generics.CreateAPIView):
    serializer_class = HotelImageSerializer
    permission_classes = [IsManagerOfHotel | IsOwnerofHotel]

    def perform_create(self, serializer):
        hotel = self.kwargs.get('hotel_id')
        serializer.save(hotel=hotel)

class HotelImageUpdateView(generics.UpdateAPIView):
    serializer_class = HotelImageSerializer
    permission_classes = [IsManagerOfHotel | IsOwnerofHotel]
    lookup_field = 'pk'

    def get_queryset(self):
        hotel_id = self.kwargs.get('hotel_id')
        return Room.objects.filter(hotel_id=hotel_id)

    def perform_update(self, serializer):
        serializer.save() 

class HotelImageDestroyView(generics.DestroyAPIView):
    serializer_class = HotelImageSerializer
    permission_classes = [IsManagerOfHotel | IsOwnerofHotel]
    lookup_field = 'pk'

    def get_queryset(self):
        hotel_id = self.kwargs.get('hotel_id')
        return Room.objects.filter(hotel_id=hotel_id)
    
class HotelImageViewSets(viewsets.ReadOnlyModelViewSet):
    serializer_class = HotelImageSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        hotel_id = self.kwargs.get('hotel_id')  
        return Image.objects.filter(hotel_id=hotel_id, imageable_type='Hotel')
