from django.shortcuts import render
from .serializers import UserSerializer
from .models import User
from rest_framework import viewsets
from rest_framework import generics, permissions
from .permissions import IsOwner, IsManager

# Create your views here.

class UserProfileView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated, IsOwner()]

    # def get_queryset(self):
    #     user = self.request.user
    #     if getattr(user, 'role', '') == 'manager':
    #         return User.objects.all()
    #     return User.objects.filter(id=user.id)
    
    # def get_permissions(self):
    #     if self.action == 'create':
    #         return [permissions.AllowAny()]

    # permission_classes = [IsOwner()]

    def get_queryset(self):
        user = self.request.user
        if user.role == "manager":
            return User.objects.all()
        else:
            return User.objects.get(id=self.request.user.id)
        
    def get_permissions(self):
        if self.action == 'create':
            return [IsManager()]
        elif self.action in ['retrieve', 'destroy']:
            return [IsManager(), IsOwner()]
        elif self.action in ['update', 'partial_update',]:
            return [IsOwner()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        # Example: auto-set the owner/user
        serializer.save()

    def perform_update(self, serializer):
        # Optional: log or customize save behavior
        serializer.save()

    def perform_destroy(self, instance):
        # Optional: log deletion
        instance.delete()