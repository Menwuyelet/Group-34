from rest_framework import serializers
from .models import User
from django.db import transaction

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'password']

    @transaction.atomic
    def create(self, validated_data):
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        email = validated_data.pop('email')
        password = validated_data.pop('password')

        if not email:
            raise ValueError("Email must be provided.")
        if not first_name:
            raise ValueError("First Name must be provided.")
        if not last_name:
            raise ValueError("Last Name must be provided.")
        
        user = User.objects.create(email=email, first_name=first_name, last_name=last_name, **validated_data)
        user.set_password(password)
        user.save()
        return user

    @transaction.atomic
    def update(self, instance, validated_data):
        first_name = validated_data.pop('first_name', None)
        last_name = validated_data.pop('last_name', None)
        email = validated_data.pop('email', None)
        password = validated_data.pop('password', None)

        if email:
            instance.email=email
        if first_name:
            instance.first_name=first_name
        if last_name:
            instance.last_name=last_name
        if password and password != instance.password:
            instance.set_password(password)
        
        instance.save()
        return instance
            