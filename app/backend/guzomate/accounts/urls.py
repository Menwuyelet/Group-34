from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include
from .views import GuestRetrieveUpdateDestroyView, GuestCreateView, GuestListView, OwnerCreateView, OwnerListView, OwnerRetrieveUpdateDestroyView, AdminViewSets
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.routers import DefaultRouter


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

urlpatterns = [
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('guest/create/', GuestCreateView.as_view(), name='user_create'),
    path('guest/list/', GuestListView.as_view(), name='user_list'),
    path('guest/<uuid:id>/', GuestRetrieveUpdateDestroyView.as_view(), name='user_detail'),
    path('admin/owners/list/', OwnerListView.as_view(), name='owners'),
    path('admin/owners/create/', OwnerCreateView.as_view(), name='create_owner'),
    path('admin/owners/<uuid:id>/', OwnerRetrieveUpdateDestroyView.as_view(), name='owner_detail'),
    path('admin/', include(router.urls)),
]