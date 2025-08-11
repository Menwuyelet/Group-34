from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from .views import UserProfileView, UserProfileCreateView, UserListView





urlpatterns = [
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/create/', UserProfileCreateView.as_view(), name='user_create'),
    path('user/list/', UserListView.as_view(), name='user_list'),
    path('user/<uuid:pk>', UserProfileView.as_view(), name='user_detail'),
]