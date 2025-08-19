from django.urls import path
from accounts.views import StaffListView, StaffCreateView, StaffRetrieveUpdateDestroyView
from .views import (
                    ## hotel
                    HotelCreateView, 
                    HotelDestroyView, 
                    HotelViewSet, 
                    HotelUpdateView, 
                    ## room
                    RoomCreateView,
                    RoomDestroyView,
                    RoomUpdateView,
                    RoomViewSets,
                    ## Event
                    EventCreateView,
                    EventUpdateView, 
                    EventDestroyView, 
                    EventViewSets,
                    ## Hotel Amenity
                    AmenityCreateView, 
                    AmenityUpdateView, 
                    AmenityDestroyView, 
                    AmenityViewSets,
                    ## Room Amenity
                    RoomAmenityViewSets,
                    RoomAmenityCreateView,
                    RoomAmenityUpdateView,
                    RoomAmenityDestroyView,
                    ## hotel image
                    HotelImageCreateView,
                    HotelImageDestroyView,
                    HotelImageUpdateView,
                    HotelImageViewSets,
                    ## Room image
                    RoomImageListView,
                    RoomImageDetailView,
                    RoomImageCreateView,
                    RoomImageUpdateView,
                    RoomImageDestroyView,
                    ## Event image
                    EventImageListView, 
                    EventImageDetailView, 
                    EventImageCreateView,
                    EventImageUpdateView, 
                    EventImageDestroyView
                    )

## hotel viewSets
hotel_list = HotelViewSet.as_view({'get': 'list'})
hotel_detail = HotelViewSet.as_view({'get': 'retrieve'})
## room viewSets
room_list = RoomViewSets.as_view({'get': 'list'})
room_detail = RoomViewSets.as_view({'get': 'retrieve'})
## hotelImage viewSets
hotel_image_list = HotelImageViewSets.as_view({'get': 'list'})
hotel_image_detail = HotelImageViewSets.as_view({'get': 'retrieve'})


urlpatterns = [
    ## hotel staff
    path(
        'hotel/<uuid:hotel_id>/staff/list/', 
            StaffListView.as_view(), name='list_staff'
        ),
    path(
        'hotel/<uuid:hotel_id>/staff/',
            StaffCreateView.as_view(), name='create_staff'
        ),
    path(
            'hotel/<uuid:hotel_id>/staff/<uuid:staff_id>', StaffRetrieveUpdateDestroyView.as_view(), name='retrieve_staff'
        ),

    ## hotel
    path(
            'hotel/create/', HotelCreateView.as_view(), name='create_hotel'
        ),
    path(
            'hotel/list/', hotel_list, name='list_hotels'
        ),
    path(
            'hotel/<uuid:hotel_id>/retrieve/', hotel_detail, name='retrieve_hotel'
        ),
    path(
            'hotel/<uuid:hotel_id>/update/', HotelUpdateView.as_view(), name='update_hotel'
        ),
    path(
            'hotel/<uuid:hotel_id>/delete/', HotelDestroyView.as_view(), name='delete_hotel'
        ),
   
    ## room
    path(
            'hotel/<uuid:hotel_id>/rooms/', room_list, name='list_rooms'
        ),
    path(
            'hotel/<uuid:hotel_id>/retrieve-room/<uuid:room_id>', room_detail, name='retrieve_room'
        ),
    path(
            'hotel/<uuid:hotel_id>/create-room/', RoomCreateView.as_view(), name='create_room'
        ),
    path(
            'hotel/<uuid:hotel_id>/update-room/<uuid:room_id>', RoomUpdateView.as_view(), name='update_room'
        ),
    path(
            'hotel/<uuid:hotel_id>/delete-room/<uuid:room_id>', RoomDestroyView.as_view(), name='delete_room'
        ),
    
    ## Event
    path(
            'hotel/<uuid:hotel_id>/events/', EventViewSets.as_view({'get': 'list'}), name='list_events'
        ),
    path(
            'hotel/<uuid:hotel_id>/event/<uuid:event_id>/', EventViewSets.as_view({'get': 'retrieve'}), name='retrieve_event'
        ),
    path(
            'hotel/<uuid:hotel_id>/event/create/', EventCreateView.as_view(), name='create_event'
        ),
    path(
            'hotel/<uuid:hotel_id>/event/<uuid:event_id>/update/', EventUpdateView.as_view(), name='update_event'
        ),
    path(
            'hotel/<uuid:hotel_id>/event/<uuid:event_id>/delete/', EventDestroyView.as_view(), name='delete_event'
        ),
   
    ## Hotel Amenity
    path(
            'hotel/<uuid:hotel_id>/amenities/', AmenityViewSets.as_view({'get': 'list'}), name='list_amenities'
        ),
    path(
            'hotel/<uuid:hotel_id>/amenity/<uuid:amenity_id>/', AmenityViewSets.as_view({'get': 'retrieve'}), name='retrieve_amenity'
        ),
    path(
            'hotel/<uuid:hotel_id>/amenity/create/', AmenityCreateView.as_view(), name='create_amenity'
        ),
    path(
            'hotel/<uuid:hotel_id>/amenity/<uuid:amenity_id>/update/', AmenityUpdateView.as_view(), name='update_amenity'
        ),
    path(
            'hotel/<uuid:hotel_id>/amenity/<uuid:amenity_id>/delete/', AmenityDestroyView.as_view(), name='delete_amenity'
        ),
    
    ## Room Amenity
    path(
            'hotel/<uuid:hotel_id>/room/<uuid:room_id>/amenities/',RoomAmenityViewSets.as_view({'get': 'list'}), name='list_room_amenities'
        ),
    path(
            'hotel/<uuid:hotel_id>/room/<uuid:room_id>/amenity/<uuid:amenity_id>/', RoomAmenityViewSets.as_view({'get': 'retrieve'}), name='retrieve_room_amenity'
        ),
    path(
            'hotel/<uuid:hotel_id>/room/<uuid:room_id>/amenity/create/', RoomAmenityCreateView.as_view(), name='create_room_amenity'
        ),
    path(
            'hotel/<uuid:hotel_id>/room/<uuid:room_id>/amenity/<uuid:amenity_id>/update/', RoomAmenityUpdateView.as_view(), name='update_room_amenity'
        ),
    path(
            'hotel/<uuid:hotel_id>/room/<uuid:room_id>/amenity/<uuid:amenity_id>/delete/', RoomAmenityDestroyView.as_view(), name='delete_room_amenity'
        ),
    
    ## hotel image
    path(
            'hotel/<uuid:hotel_id>/images/', hotel_image_list, name='list_hotel_images'
        ),
    path(
            'hotel/<uuid:hotel_id>/image/<uuid:image_id>', hotel_image_detail, name='retrieve_hotel_image'
        ),
    path(
            'hotel/<uuid:hotel_id>/image/create-image/', HotelImageCreateView.as_view(), name='create_hotel_image'
        ),
    path(
            'hotel/<uuid:hotel_id>/image/<uuid:image_id>/update-image/', HotelImageUpdateView.as_view(), name='update_hotel_image'
        ),
    path(
            'hotel/<uuid:hotel_id>/image/<uuid:image_id>/delete-image/', HotelImageDestroyView.as_view(), name='delete_hotel_image'
        ),

    ## Room image
    path(
            'hotel/<uuid:hotel_id>/room/<uuid:room_id>/images/', RoomImageListView.as_view(), name='list_room_images'
        ),
    path(
            'hotel/<uuid:hotel_id>/room/<uuid:room_id>/image/<uuid:image_id>/', RoomImageDetailView.as_view(), name='retrieve_room_image'
        ),
    path(
            'hotel/<uuid:hotel_id>/room/<uuid:room_id>/image/create/', RoomImageCreateView.as_view(), name='create_room_image'
        ),
    path(
            'hotel/<uuid:hotel_id>/room/<uuid:room_id>/image/<uuid:image_id>/update/', RoomImageUpdateView.as_view(), name='update_room_image'
        ),
    path(
            'hotel/<uuid:hotel_id>/room/<uuid:room_id>/image/<uuid:image_id>/delete/', RoomImageDestroyView.as_view(), name='delete_room_image'
        ),

    ## Event image
    path(
            'hotel/<uuid:hotel_id>/event/<uuid:event_id>/images/', EventImageListView.as_view(), name='list_event_images'
        ),
    path(
            'hotel/<uuid:hotel_id>/event/<uuid:event_id>/image/<uuid:image_id>/', EventImageDetailView.as_view(), name='retrieve_event_image'
        ),
    path(
            'hotel/<uuid:hotel_id>/event/<uuid:event_id>/image/create/', EventImageCreateView.as_view(), name='create_event_image'
        ),
    path(
            'hotel/<uuid:hotel_id>/event/<uuid:event_id>/image/<uuid:image_id>/update/', EventImageUpdateView.as_view(), name='update_event_image'
        ),
    path(
            'hotel/<uuid:hotel_id>/event/<uuid:event_id>/image/<uuid:image_id>/delete/', EventImageDestroyView.as_view(), name='delete_event_image'
        ),

]


## the url for the viewset of the rooms in the hotel


# urlpatterns = [
#     # list all rooms for a hotel
#     path('hotels/<uuid:hotel_id>/rooms/', room_list, name='hotel-rooms'),
    
#     # detail for a single room in a hotel
#     path('hotels/<uuid:hotel_id>/rooms/<uuid:pk>/', room_detail, name='hotel-room-detail'),
# ]