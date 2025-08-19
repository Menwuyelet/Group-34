from rest_framework.permissions import BasePermission
from hotel.models import Hotel
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

        # 1. Only receptionist are allowed
        if getattr(user, 'role', '').lower() != 'receptionist':
            return False

        # 2. Get hotel_id from URL
        hotel_id = view.kwargs.get('hotel_id')
        if not hotel_id:
            return False

        # 3. Check hotel exists
        try:
            hotel = Hotel.objects.get(id=hotel_id)
        except Hotel.DoesNotExist:
            return False

        # 4. Check if the user is in hotel staff
        return hotel.staff_members.filter(id=user.id).exists()

class IsManagerOfHotel(BasePermission):
    message = "You are not allowed to access this hotel data."

    def has_permission(self, request, view):
        user = request.user

        # 1. Only managers are allowed
        if getattr(user, 'role', '').lower() != 'manager':
            return False

        # 2. Get hotel_id from URL
        hotel_id = view.kwargs.get('hotel_id')
        if not hotel_id:
            return False

        # 3. Check hotel exists
        try:
            hotel = Hotel.objects.get(id=hotel_id)
        except Hotel.DoesNotExist:
            return False

        # 4. Check if the user is in hotel staff
        return hotel.staff_members.filter(id=user.id).exists()
class IsOwnerofHotel(BasePermission):
    message = "You are not allowed to access this hotel data."
    
    def has_permission(self, request, view):
        user = request.user
       
        if getattr(user, 'role', '').lower() != 'owner':
            return False
        
        hotel_id = view.kwargs.get('hotel_id')
        if not hotel_id:
            return False

        try:
            hotel = Hotel.objects.get(id=hotel_id)
        except Hotel.DoesNotExist:
            return False

        return str(hotel.owner) == str(user.id)