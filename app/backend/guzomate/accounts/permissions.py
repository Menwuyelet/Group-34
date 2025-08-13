from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'role', '').lower() == 'admin'

class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'role', '').lower() == 'staff'

class IsManagerOfHotel(BasePermission):
    message = "You are not allowed to access this hotel data."

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated or getattr(user, 'role', '').lower() != 'manager':
            return False

        hotel_id = view.kwargs.get('pk')
        return hotel_id and getattr(user.hotel, 'id', None) == hotel_id
    

class IsGuest(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'role', '').lower() == 'guest'
    
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user
    
class IsOwnerofHotel(BasePermission):
    message = "You are not allowed to access this hotel data."

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated or getattr(user, 'role', '').lower() != 'owner':
            return False

        hotel_id = view.kwargs.get('pk')
        return hotel_id and getattr(user.hotel, 'id', None) == hotel_id