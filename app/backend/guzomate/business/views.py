from django.shortcuts import render
from rest_framework import generics, viewsets, serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import ReviewSerializer, BookingSerializer
from hotel.models import Hotel, Room
from accounts.models import User
from accounts.permissions import IsOwnerOfInstance, IsAdmin
from .models import Review, Booking

## Review
class ReviewCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        hotel_id = self.kwargs.get('hotel_id')
        hotel = Hotel.objects.get(id=hotel_id)
        user = self.request.user
        serializer.save(hotel=hotel, user=user)

class UserReviewUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOfInstance]
    serializer_class = ReviewSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'review_id'

    def get_queryset(self):
        user = self.request.user
        return Review.objects.filter(user=user)

class UserReviewViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOfInstance]
    serializer_class = ReviewSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'review_id'

    def get_queryset(self):
        user = self.request.user
        return Review.objects.filter(user=user)
    
class UserReviewDelete(generics.DestroyAPIView): 
    permission_classes = [IsAdmin | IsOwnerOfInstance]
    serializer_class = ReviewSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'review_id'

    def get_queryset(self):
        user = self.request.user
        return Review.objects.filter(user=user)

class HotelReviewViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ReviewSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'review_id'

    def get_queryset(self):
        hotel_id = self.kwargs.get('hotel_id')
        hotel = Hotel.objects.get(id=hotel_id)
        return Review.objects.filter(hotel=hotel)

## Booking 

class UserBookingCreateView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Get hotel and room from URL params or request data
        hotel_id = self.kwargs.get("hotel_id")
        room_id = self.kwargs.get("room_id")

        hotel = Hotel.objects.get(id=hotel_id)
        room = Room.objects.get(id=room_id, hotel=hotel)

        serializer.save(
            user=self.request.user,
            hotel=hotel,
            room=room,
            booking_source="Online"
        )

class UserBookingUpdateView(generics.UpdateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, IsOwnerOfInstance]
    lookup_field = 'id'
    lookup_url_kwarg = 'booking_id'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)


class UserBookingViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOfInstance | IsAdmin]
    serializer_class = BookingSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'booking_id'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)


# class BookingDelete(generics.DestroyAPIView): 
#     permission_classes = [IsAdmin | IsOwnerOfInstance]
#     serializer_class = ReviewSerializer
#     lookup_field = 'id'
#     lookup_url_kwarg = 'review_id'

#     def get_queryset(self):
#         user = self.request.user
#         return Review.objects.filter(user=user)





# Create your views here.
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
