from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include
from .views import (
                    GuestRetrieveUpdateDestroyView, 
                    GuestCreateView, 
                    GuestListView, 
                    OwnerCreateView, 
                    OwnerListView, 
                    OwnerRetrieveUpdateDestroyView, 
                    AdminViewSets,
                    )
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.routers import DefaultRouter
from business.views import (    
                                UserReviewUpdateView, 
                                UserReviewViewSet, 
                                UserReviewDelete,
                                CityCreateView,
                                CityUpdateView,
                                CityDestroyView,
                                CityViewSets,
                                CityImageReadOnlyViewSet,
                                CityImageDestroyView,
                                CityImageUpdateView,
                                LocalAttractionDestroyView,
                                LocalAttractionUpdateView,
                                LocalAttractionCreateView,
                                CityLocalAttractionReadOnlyViewSet
                            )


router = DefaultRouter()
router.register(r'admins', AdminViewSets, basename='admins')

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Add custom data
        data['user'] = {
            "id": self.user.id,
            "email": self.user.email,
            "role": self.user.role,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
        }
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

review_list = UserReviewViewSet.as_view({'get': 'list'})
review_detail = UserReviewViewSet.as_view({'get': 'retrieve'})

city_list = CityViewSets.as_view({'get': 'list'})
city_detail = CityViewSets.as_view({'get': 'retrieve'})

city_image_list = CityImageReadOnlyViewSet.as_view({'get': 'list'})
city_image_detail = CityImageReadOnlyViewSet.as_view({'get': 'retrieve'})

local_attraction_list = CityLocalAttractionReadOnlyViewSet.as_view({'get': 'list'})
local_attraction_retrieve = CityLocalAttractionReadOnlyViewSet.as_view({'get': 'retrieve'})

urlpatterns = [
    ## auth
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ## guest
    path('guest/create/', GuestCreateView.as_view(), name='create_user'),
    path('guest/<uuid:id>/', GuestRetrieveUpdateDestroyView.as_view(), name='retrieve_user'),
    path('guest/<uuid:id>/review/<uuid:review_id>/update/', UserReviewUpdateView.as_view(), name='update_review'),
    path('guest/<uuid:id>/reviews/', review_list, name='list_reviews'),
    path('guest/<uuid:id>/review/<uuid:review_id>/detail/', review_detail, name='retrieve_reviews'),
    path('guest/<uuid:id>/review/<uuid:review_id>/delete/', UserReviewDelete.as_view(), name='delete_review'),
    path('guest/cities/', city_list, name='list_cities'),
    path('guest/city/<uuid:city_id>/', city_detail, name='retrieve_city'),
    path('guest/city/<uuid:city_id>/images/list/', city_image_list, name='city_image_list'),
    path('guest/city/<uuid:city_id>/image/<uuid:image_id>/retrieve/', city_image_detail, name='city_image_retrieve'),
    path('guest/city/<uuid:city_id>/attractions/list/', local_attraction_list, name='list_city_attractions'),
    path('guest/city/<uuid:city_id>/attraction/detail/', local_attraction_retrieve, name='retrieve_city_attractions'),

   
    # path('guest/<uuid:id>/bookings/list', booking_list, name='user_booking_list'),
    # path('guest/<uuid:id>/booking/<uuid:booking_id>', booking_detail, name='user_booking_detail'),
    # path('guest/<uuid:id>/booking/<uuid:booking_id>/update/', UserBookingUpdateView.as_view(), name='update_user_booking'),
    
    ## admin
    path('admin/', include(router.urls)),
    ### owner
    path('admin/owners/create/', OwnerCreateView.as_view(), name='create_owner'),
    path('admin/owners/list/', OwnerListView.as_view(), name='list_owners'),
    path('admin/owners/<uuid:id>/', OwnerRetrieveUpdateDestroyView.as_view(), name='retrieve_owner'),
    ### guest
    path('admin/guest/list/', GuestListView.as_view(), name='list_users'),
    path('admin/guest/<uuid:id>/', GuestRetrieveUpdateDestroyView.as_view(), name='retrieve_user'),
    ### city
    path('admin/cities/create/', CityCreateView.as_view(), name='create_city'),
    path('admin/city/<uuid:city_id>/update/', CityUpdateView.as_view(), name='update_city'),
    path('admin/city/<uuid:city_id>/delete/', CityDestroyView.as_view(), name='delete_city'),
    path('admin/city/<uuid:city_id>/image/create/', CityImageUpdateView.as_view(), name='create_city_image'),
    path('admin/city/<uuid:city_id>/image/<uuid:image_id>/delete/', CityImageDestroyView.as_view(), name='city_image_delete'),
    path('admin/city/<uuid:city_id>/image/<uuid:image_id>/update/', CityImageUpdateView.as_view(), name='city_image_retrieve'),
    path('admin/city/<uuid:city_id>/attraction/create/', LocalAttractionCreateView.as_view(), name='create_city_attraction'),
    path('admin/city/<uuid:city_id>/attraction/<uuid:attraction_id>/update/', LocalAttractionUpdateView.as_view(), name='update_city_attraction'),
    path('admin/city/<uuid:city_id>/attraction/<uuid:attraction_id>/delete/', LocalAttractionDestroyView.as_view(), name='delete_city_attraction'),

   
]