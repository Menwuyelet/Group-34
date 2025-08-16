from django.urls import path
from accounts.views import StaffListView, StaffCreateView, StaffRetrieveUpdateDestroyView
# from .views import HotelListCreateView, HotelRetrieveUpdateDestroyView



urlpatterns = [
    path('hotel/<uuid:hotel_id>/staff/list/', StaffListView.as_view(), name='staff_list'),
    path('hotel/<uuid:hotel_id>/staff/', StaffCreateView.as_view(), name='staff_create'),
    path('hotel/<uuid:hotel_id>/staff/<uuid:id>', StaffRetrieveUpdateDestroyView.as_view(), name='staff_detail'),
    # path('hotel/list/', HotelListCreateView.as_view(), name='create_hotel'),
    # path('hotel/<uuid:hotel_id>', HotelRetrieveUpdateDestroyView.as_view(), name='list_hotel'),
#     path('guest/<uuid:pk>', GuestRetrieveUpdateDestroyView.as_view(), name='user_detail'),
]


## the url for the viewset of the rooms in the hotel
# room_list = RoomViewSets.as_view({'get': 'list'})
# room_detail = RoomViewSets.as_view({'get': 'retrieve'})

# urlpatterns = [
#     # list all rooms for a hotel
#     path('hotels/<uuid:hotel_id>/rooms/', room_list, name='hotel-rooms'),
    
#     # detail for a single room in a hotel
#     path('hotels/<uuid:hotel_id>/rooms/<uuid:pk>/', room_detail, name='hotel-room-detail'),
# ]