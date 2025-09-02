from django.shortcuts import render
from .permissions import IsAdmin, IsOwner, IsManagerOfHotel,  IsOwnerofHotel
from .serializers import StaffSerializer, GuestSerializer, OwnerAdminSerializer
from .models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets 
from hotel.models import Hotel
from rest_framework.exceptions import PermissionDenied
# Create your views here.

class GuestRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GuestSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsAdmin]
    lookup_field = 'id'
    

    def get_queryset(self):
        return User.objects.all()

    def perform_update(self, serializer):
        serializer.save()
    
    def perform_destroy(self, instance):
        instance.delete()
    
class GuestCreateView(generics.CreateAPIView):
    serializer_class = GuestSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save()
class GuestListView(generics.ListAPIView):
    serializer_class = GuestSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    # permission_classes = [AllowAny]
    def get_queryset(self):
        return User.objects.filter(role="Guest")

## Staff users
class StaffRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsManagerOfHotel | IsOwnerofHotel]
    # permission_classes = [AllowAny]
    serializer_class = StaffSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'staff_id'

    def get_queryset(self):
        return User.objects.filter(role__in=['Manager', 'Receptionist'])
        
    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

class StaffCreateView(generics.CreateAPIView):
    # permission_classes = [AllowAny]
    serializer_class = StaffSerializer
    permission_classes = [IsManagerOfHotel | IsOwnerofHotel]

    def perform_create(self, serializer):
        hotel_id = self.kwargs.get('hotel_id')
        hotel = Hotel.objects.get(id=hotel_id)
        
        role = serializer.validated_data.get('role')
        if self.request.user.role == 'Manager' and role == 'Manager':
            raise PermissionDenied("Manager cannot create another manager.")
        serializer.save(hotel=hotel)

class StaffListView(generics.ListAPIView):
    serializer_class = StaffSerializer
    permission_classes = [IsManagerOfHotel | IsOwnerofHotel]
    # permission_classes = [AllowAny]
    def get_queryset(self):
        return User.objects.filter(role__in=['Manager', 'Receptionist'])

## owner
class OwnerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin]
    serializer_class = OwnerAdminSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return User.objects.filter(role='Owner')
    
    def perform_update(self, serializer):
        serializer.save()
    
    def perform_destroy(self, instance):
        instance.delete()
    
class OwnerCreateView(generics.CreateAPIView):
    serializer_class = OwnerAdminSerializer
    permission_classes = [IsAdmin]

    def perform_create(self, serializer):
        role="Owner"
        serializer.save(role=role)

class OwnerListView(generics.ListAPIView):
    serializer_class = OwnerAdminSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        return User.objects.filter(role='Owner')
    
## Admin
class AdminViewSets(viewsets.ModelViewSet):
    serializer_class = OwnerAdminSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'id'

    def get_queryset(self):
        return User.objects.filter(role='Admin')

    def perform_create(self, serializer):
        role = "Admin"
        serializer.save(role=role)
    
    def perform_destroy(self, instance):
        instance.delete()
    