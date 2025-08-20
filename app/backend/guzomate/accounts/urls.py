from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include
from .views import GuestRetrieveUpdateDestroyView, GuestCreateView, GuestListView, OwnerCreateView, OwnerListView, OwnerRetrieveUpdateDestroyView, AdminViewSets
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.routers import DefaultRouter
from business.views import UserReviewUpdateView, UserReviewViewSet, UserReviewDelete, UserBookingViewSet, UserBookingUpdateView


router = DefaultRouter()
router.register(r'admins', AdminViewSets, basename='admins')

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Add custom data
        data['id'] = self.user.id
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

review_list = UserReviewViewSet.as_view({'get': 'list'})
review_detail = UserReviewViewSet.as_view({'get': 'retrieve'})

booking_list = UserBookingViewSet.as_view({'get': 'list'})
booking_detail = UserBookingViewSet.as_view({'get': 'retrieve'})

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
    path('guest/<uuid:id>/bookings/list', booking_list, name='user_booking_list'),
    path('guest/<uuid:id>/booking/<uuid:booking_id>', booking_detail, name='user_booking_detail'),
    path('guest/<uuid:id>/booking/<uuid:booking_id>/update/', UserBookingUpdateView.as_view(), name='update_user_booking'),
    
    ## admin
    path('admin/guest/list/', GuestListView.as_view(), name='list_users'),
    path('admin/guest/<uuid:id>/', GuestRetrieveUpdateDestroyView.as_view(), name='retrieve_user'),
    path('admin/owners/list/', OwnerListView.as_view(), name='list_owners'),
    path('admin/owners/create/', OwnerCreateView.as_view(), name='create_owner'),
    path('admin/owners/<uuid:id>/', OwnerRetrieveUpdateDestroyView.as_view(), name='retrieve_owner'),
    path('admin/', include(router.urls)),
]