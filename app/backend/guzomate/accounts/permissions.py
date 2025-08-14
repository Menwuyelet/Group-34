from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return getattr(request.user, 'role', '').lower() == 'admin'
    
class IsGuest(BasePermission):
    def has_permission(self, request, view):
        return getattr(request.user, 'role', '').lower() == 'guest'

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user


## hotel perms
class IsReceptionist(BasePermission):
    message = "You are not allowed to access this hotel data."
    def has_permission(self, request, view):
        user = request.user
        if getattr(user, 'role', '').lower() != 'receptionist':
            return False
        hotel_id = view.kwargs.get('pk')
        return hotel_id and getattr(user.hotel, 'id', None) == hotel_id

class IsManagerOfHotel(BasePermission):
    message = "You are not allowed to access this hotel data."

    def has_permission(self, request, view):
        user = request.user
        if getattr(user, 'role', '').lower() != 'manager':
            return False

        hotel_id = view.kwargs.get('pk')
        return hotel_id and getattr(user.hotel, 'id', None) == hotel_id
    

class IsOwnerofHotel(BasePermission):
    message = "You are not allowed to access this hotel data."

    def has_permission(self, request, view):
        user = request.user
        if getattr(user, 'role', '').lower() != 'owner':
            return False

        hotel_id = view.kwargs.get('pk')
        return hotel_id and getattr(user.hotel, 'id', None) == hotel_id