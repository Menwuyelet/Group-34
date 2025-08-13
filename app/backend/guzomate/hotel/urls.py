from django.urls import path
from accounts.views import StaffListView, StaffCreateView, StaffRetrieveUpdateDestroyView





urlpatterns = [
    path('hotel/<uuid:pk>/staff/list/', StaffListView.as_view(), name='staff_list'),
    path('hotel/<uuid:pk>/staff/', StaffCreateView.as_view(), name='staff_create'),
    path('hotel/<uuid:pk>/staff/<uuid:id>', StaffRetrieveUpdateDestroyView.as_view(), name='staff_detail'),
    
#     path('guest/<uuid:pk>', GuestRetrieveUpdateDestroyView.as_view(), name='user_detail'),
]