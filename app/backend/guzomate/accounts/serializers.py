from rest_framework import serializers
from .models import User
from django.db import transaction
import re
from django.contrib.auth.password_validation import validate_password

class StaffSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'role','picture', 'gender', 'nationality', 'hotel', 'password']
        read_only_field = ['hotel']
    def validate_picture(self, value):
        if value == None:
            return value
        max_size = 5 * 1024 * 1024  # 5MB
        if value.content_type not in ['image/jpeg', 'image/png', 'image/gif']:
            raise serializers.ValidationError("Only JPEG, PNG, and GIF images are allowed.")
        if value.size > max_size:
            raise serializers.ValidationError("Image size should not exceed 5MB.")
        return value

    def validate_phone(self, value):
        if not re.match(r'^\+?\d{7,15}$', value):
            raise serializers.ValidationError("Invalid phone number format.")
        return value

    def validate_password(self, value):
        validate_password(value)

        if not re.search(r'[A-Za-z]', value):
            raise serializers.ValidationError("Password must contain at least one letter.")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one number.")
        if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', value):
            raise serializers.ValidationError("Password must contain at least one special character.")

        return value

    def validate(self, attrs):
        role = attrs.get('role')
        hotel = attrs.get('hotel')

        if role in ["Owner", "Manager", "Receptionist"] and not hotel:
            raise serializers.ValidationError({
                "hotel": "Hotel must be provided for for this user."
            })
        if role in ['Guest', 'Admin']:
            raise serializers.ValidationError({
                "hotel": "User can not be Guest or Admin, please choose different role."
            })

        return attrs
    
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
        email = validated_data.pop('email', None)
        password = validated_data.pop('password', None)
        role = validated_data.pop('role', None)
        phone = validated_data.pop('phone', None)

        if email:
            instance.email=email
        if phone:
            clean_phone = self.validate_phone(phone)
            instance.phone=clean_phone
        if password and password != instance.password:
            instance.set_password(password)

        picture = validated_data.pop('picture', None)
        if picture is not None:
            instance.picture = picture 

        if role:
            instance.role = role
            if role in ['Guest', 'Admin']:
                instance.hotel = None
            elif role in ["Owner", "Manager", "Receptionist"] and instance.hotel is None:
                raise ValueError("Hotel must be provided for managers and staff.")

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
            

class GuestSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)
    role = serializers.HiddenField(default='Guest')
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'role','picture', 'gender', 'nationality', 'password']
        read_only_fields = ['id']

    def validate_picture(self, value):
        if value == None:
            return value
        max_size = 5 * 1024 * 1024  # 5MB
        if value.content_type not in ['image/jpeg', 'image/png', 'image/gif']:
            raise serializers.ValidationError("Only JPEG, PNG, and GIF images are allowed.")
        if value.size > max_size:
            raise serializers.ValidationError("Image size should not exceed 5MB.")
        return value

    def validate_phone(self, value):
        if not re.match(r'^\+?\d{7,15}$', value):
            raise serializers.ValidationError("Invalid phone number format.")
        return value

    def validate_password(self, value):
        validate_password(value)

        if not re.search(r'[A-Za-z]', value):
            raise serializers.ValidationError("Password must contain at least one letter.")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one number.")
        if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', value):
            raise serializers.ValidationError("Password must contain at least one special character.")

        return value

    
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
        email = validated_data.pop('email', None)
        password = validated_data.pop('password', None)
        role = validated_data.pop('role', None)
        phone = validated_data.pop('phone', None)

        if email:
            instance.email=email
        if phone:
            clean_phone = self.validate_phone(phone)
            instance.phone=clean_phone
        if password and password != instance.password:
            instance.set_password(password)

        picture = validated_data.pop('picture', None)
        if picture is not None:
            instance.picture = picture 

        if role:
            instance.role = role
            if role in ['Guest', 'Admin']:
                instance.hotel = None
            elif role in ["Owner", "Manager", "Receptionist"] and instance.hotel is None:
                raise ValueError("Hotel must be provided for managers and staff.")

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
            