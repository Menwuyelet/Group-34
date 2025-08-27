from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import ReviewSerializer, CitySerializer, CityImageSerializer, LocalAttractionSerializer, HotelCitiesSerializers, FavoriteSerializer
from hotel.models import Hotel, Image
from accounts.permissions import IsOwnerOfInstance, IsAdmin, IsManagerOfHotel, IsOwnerofHotel
from .models import Review, City, LocalAttraction, HotelCities, Favorite

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

## City
class CityCreateView(generics.CreateAPIView):
    serializer_class = CitySerializer
    permission_classes = [IsAdmin] # change to custom permission if needed

    def perform_create(self, serializer):
        serializer.save()

class CityUpdateView(generics.UpdateAPIView):
    serializer_class = CitySerializer
    permission_classes = [IsAdmin]
    lookup_field = 'id'
    lookup_url_kwarg = 'city_id'

    def get_queryset(self):
        return City.objects.all()

    def perform_update(self, serializer):
        serializer.save()

class CityDestroyView(generics.DestroyAPIView):
    serializer_class = CitySerializer
    permission_classes = [IsAdmin]
    lookup_field = 'id'
    lookup_url_kwarg = 'city_id'

    def get_queryset(self):
        return City.objects.all()

class CityViewSets(viewsets.ReadOnlyModelViewSet):
    serializer_class = CitySerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'
    lookup_url_kwarg = 'city_id'

    def get_queryset(self):
        return City.objects.all().order_by('name')

## City Image
class CityImageCreateView(generics.CreateAPIView):
    permission_classes = [IsAdmin]
    serializer_class = CityImageSerializer

    def perform_create(self, serializer):
        city_id = self.kwargs['city_id']
        city = City.objects.get(id=city_id)
        serializer.save(
            imageable_type='City',
            imageable_id=city.id,
            city=city_id,
            city_name=city.name
        )

class CityImageReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CityImageSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"
    lookup_url_kwarg = "image_id"

    def get_queryset(self):
        city_id = self.kwargs['city_id']
        city = City.objects.get(id=city_id)
        return Image.objects.filter(
            imageable_type='City',
            imageable_id=city_id,
            city=city_id,
            city_name=city.name
        ).order_by("uploaded_at")
    
class CityImageUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAdmin]
    serializer_class = CityImageSerializer
    lookup_field = "id"
    lookup_url_kwarg = "image_id"

    def get_queryset(self):
        city_id = self.kwargs['city_id']
        return Image.objects.filter(
            city=city_id,
            imageable_id=city_id,
            imageable_type='City'
        )
    
class CityImageDestroyView(generics.DestroyAPIView):
    permission_classes = [IsAdmin]
    serializer_class = CityImageSerializer
    lookup_field = "id"
    lookup_url_kwarg = "image_id"

    def get_queryset(self):
        city_id = self.kwargs['city_id']
        return Image.objects.filter(
            city=city_id,
            imageable_id=city_id,
            imageable_type='City'
        )

## Local Attractions
class LocalAttractionCreateView(generics.CreateAPIView):
    permission_classes = [IsAdmin]
    # permission_classes = [AllowAny]
    serializer_class = LocalAttractionSerializer

    def perform_create(self, serializer):
        city_id = self.kwargs.get('city_id')
        city = City.objects.get(id=city_id)
        serializer.save(city=city)

class LocalAttractionUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAdmin]
    # permission_classes = [AllowAny]
    serializer_class = LocalAttractionSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "attraction_id"

    def get_queryset(self):
        city_id = self.kwargs.get('city_id')
        attraction_id = self.kwargs.get('attraction_id')
        return LocalAttraction.objects.filter(city=city_id, id=attraction_id)

class LocalAttractionDestroyView(generics.DestroyAPIView):
    permission_classes = [IsAdmin]
    serializer_class = LocalAttractionSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "attraction_id"

    def get_queryset(self):
        city_id = self.kwargs.get('city_id')
        attraction_id = self.kwargs.get('attraction_id')
        return LocalAttraction.objects.filter(city=city_id, id=attraction_id)

class CityLocalAttractionReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LocalAttractionSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'
    lookup_url_kwarg = "attraction_id"

    def get_queryset(self):
        city_id = self.kwargs['city_id']
        return LocalAttraction.objects.filter(city=city_id).order_by("name")

## Hotel City
class HotelCityCreateView(generics.CreateAPIView):
    permission_classes = [IsAdmin | IsOwnerofHotel | IsManagerOfHotel]
    serializer_class = HotelCitiesSerializers

    def perform_create(self, serializer):
        hotel_id = self.kwargs.get('hotel_id')
        serializer.save(hotel=hotel_id)

class HotelCityUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAdmin | IsOwnerofHotel | IsManagerOfHotel]
    serializer_class = HotelCitiesSerializers
    lookup_field = 'id'
    lookup_url_kwarg = "hotel_city_id"

    def get_queryset(self):
        return HotelCities.objects.all()

class HotelCityDestroyView(generics.DestroyAPIView):
    permission_classes = [IsAdmin | IsOwnerofHotel | IsManagerOfHotel]
    serializer_class = HotelCitiesSerializers
    lookup_field = 'id'
    lookup_url_kwarg = "hotel_city_id"

    def get_queryset(self):
        return HotelCities.objects.all()
    
class HotelCityListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = HotelCitiesSerializers
    lookup_field = 'id'
    lookup_url_kwarg = "hotel_id"

    def get_queryset(self):
        hotel_id = self.kwargs.get('hotel_id')
        return HotelCities.objects.filter(hotel=hotel_id).order_by('city')

## Guest Favorite 
class FavoriteCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FavoriteSerializer

    def perform_create(self, serializer):
        user = self.request.user
        hotel = self.kwargs.get('hotel_id')
        return serializer.save(hotel=hotel, user=user)

class FavoriteReadOnlyViewSets(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAdmin | IsOwnerOfInstance]
    serializer_class = FavoriteSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'favorite_id'

    def get_queryset(self):
        user = self.request.user
        favorite_id = self.kwargs.get('favorite_id', None)
        if favorite_id:
            return Favorite.objects.filter(user=user, id=favorite_id)
        return Favorite.objects.filter(user=user).order_by('created_at')

class FavoriteDestroyView(generics.DestroyAPIView):
    permission_classes = [IsOwnerOfInstance]
    serializer_class = FavoriteSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'favorite_id'

    def get_queryset(self):
        user = self.request.user
        favorite_id = self.kwargs.get('favorite_id')
        return Favorite.objects.filter(user=user, id=favorite_id)
        