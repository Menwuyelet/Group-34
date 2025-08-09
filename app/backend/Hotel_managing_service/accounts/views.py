from django.shortcuts import render
from .serializers import UserSerializer
from .models import User
from rest_framework import viewsets
from rest_framework import generics
from .permissions import IsOwner, IsManager, IsAdmin
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

# Create your views here.

class UserProfileCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsManager | IsAdmin]

    def perform_create(self, serializer):
        serializer.save()
    
class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsManager | IsOwner]

    def get_queryset(self):
        pk = self.kwargs.get('pk')  
        user = self.request.user

        if user.role == 'manager':
            return User.objects.all()
        elif user.id == pk:
            return User.objects.filter(id=user.id)
        else:
            raise PermissionDenied("You do not have permission to view this profile.")

    def perform_update(self, serializer):
        pk = self.kwargs.get('pk')  
        user = self.request.user

        if user.role == 'manager' or user.id == pk:
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to view this profile.")
    
    def perform_destroy(self, instance):
        pk = self.kwargs.get('pk')  
        user = self.request.user

        if user.role == 'manager' or user.id == pk:
            instance.delete()
        else:
            raise PermissionDenied("You do not have permission to view this profile.")

class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsManager]

    def get_queryset(self):
        return User.objects.all()
