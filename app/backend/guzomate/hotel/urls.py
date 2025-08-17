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
                    ## hotel image
                    HotelImageCreateView,
                    HotelImageDestroyView,
                    HotelImageUpdateView,
                    HotelImageViewSets
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
    path('hotel/<uuid:hotel_id>/staff/list/', StaffListView.as_view(), name='list_staff'),
    path('hotel/<uuid:hotel_id>/staff/', StaffCreateView.as_view(), name='create_staff'),
    path('hotel/<uuid:hotel_id>/staff/<uuid:staff_id>', StaffRetrieveUpdateDestroyView.as_view(), name='retrieve_staff'),

    ## hotel
    path('hotel/create/', HotelCreateView.as_view(), name='create_hotel'),
    path('hotel/list/', hotel_list, name='list_hotels'),
    path('hotel/<uuid:hotel_id>/retrieve/', hotel_detail, name='retrieve_hotel'),
    path('hotel/<uuid:hotel_id>/update/', HotelUpdateView.as_view(), name='update_hotel'),
    path('hotel/<uuid:hotel_id>/delete/', HotelDestroyView.as_view(), name='delete_hotel'),
   
    ## room
    path('hotel/<uuid:hotel_id>/rooms/', room_list, name='list_rooms'),
    path('hotel/<uuid:hotel_id>/retrieve-room/<uuid:room_id>', room_detail, name='retrieve_room'),
    path('hotel/<uuid:hotel_id>/create-room/', RoomCreateView.as_view(), name='create_room'),
    path('hotel/<uuid:hotel_id>/update-room/<uuid:room_id>', RoomUpdateView.as_view(), name='update_room'),
    path('hotel/<uuid:hotel_id>/delete-room/<uuid:room_id>', RoomDestroyView.as_view(), name='delete_room'),

    ## hotel image
    path('hotel/<uuid:hotel_id>/images/', hotel_image_list, name='list_hotel_images'),
    path('hotel/<uuid:hotel_id>/image/<uuid:image_id>', hotel_image_detail, name='retrieve_hotel_image'),
    path('hotel/<uuid:hotel_id>/image/create-image/', HotelImageCreateView.as_view(), name='create_hotel_image'),
    path('hotel/<uuid:hotel_id>/image/<uuid:image_id>/update-image/', HotelImageUpdateView.as_view(), name='update_hotel_image'),
    path('hotel/<uuid:hotel_id>/image/<uuid:image_id>/delete-image/', HotelImageDestroyView.as_view(), name='delete_hotel_image'),

    ##
   
]


## the url for the viewset of the rooms in the hotel


# urlpatterns = [
#     # list all rooms for a hotel
#     path('hotels/<uuid:hotel_id>/rooms/', room_list, name='hotel-rooms'),
    
#     # detail for a single room in a hotel
#     path('hotels/<uuid:hotel_id>/rooms/<uuid:pk>/', room_detail, name='hotel-room-detail'),
# ]