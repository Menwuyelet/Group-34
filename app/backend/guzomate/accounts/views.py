from django.shortcuts import render
from .permissions import IsAdmin, IsOwner, IsGuest, IsManagerOfHotel, IsReceptionist, IsOwnerofHotel
from .serializers import StaffSerializer, GuestSerializer
from .models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
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

    def get_queryset(self):
        return User.objects.filter(role="Guest")

## Staff users

class StaffRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwner | IsManagerOfHotel | IsOwnerofHotel]
    serializer_class = StaffSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return User.objects.filter(role__in=['Manager', 'Receptionist'])
        
def perform_update(self, serializer):
    serializer.save()

def perform_destroy(self, instance):
    instance.delete()

    
class StaffCreateView(generics.CreateAPIView):
    serializer_class = StaffSerializer
    permission_classes = [IsManagerOfHotel | IsOwnerofHotel]

    def perform_create(self, serializer):
        hotel_id = self.kwargs.get('id')
        serializer.save(hotel=hotel_id)
        
class StaffListView(generics.ListAPIView):
    serializer_class = StaffSerializer
    permission_classes = [IsManagerOfHotel | IsOwnerofHotel]

    def get_queryset(self):
        return User.objects.filter(role__in=['Manager', 'Receptionist'])


# Create your views here.

# class UserProfileCreateView(generics.CreateAPIView):
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated, IsManager | IsAdmin]

#     def perform_create(self, serializer):
#         serializer.save()
    
# class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated, IsManager | IsOwner]

#     def get_queryset(self):
#         pk = self.kwargs.get('pk')  
#         user = self.request.user

#         if user.role == 'manager':
#             return User.objects.all()
#         elif user.id == pk:
#             return User.objects.filter(id=user.id)
#         else:
#             raise PermissionDenied("You do not have permission to view this profile.")

#     def perform_update(self, serializer):
#         pk = self.kwargs.get('pk')  
#         user = self.request.user

#         if user.role == 'manager' or user.id == pk:
#             serializer.save()
#         else:
#             raise PermissionDenied("You do not have permission to view this profile.")
    
#     def perform_destroy(self, instance):
#         pk = self.kwargs.get('pk')  
#         user = self.request.user

#         if user.role == 'manager' or user.id == pk:
#             instance.delete()
#         else:
#             raise PermissionDenied("You do not have permission to view this profile.")

# class UserListView(generics.ListAPIView):
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated, IsManager]

#     def get_queryset(self):
#         return User.objects.all()
