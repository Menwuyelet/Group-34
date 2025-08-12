from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import uuid


class UserManager(BaseUserManager):
    def create_user(self, email, password,**extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError("Password must be provided")
        
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    phone = models.CharField(unique=True, max_length=15)
    role = models.CharField(choices=[
                                    ("Admin", "Admin"),
                                    ("Guest", "Guest"),
                                    ("Owner", "Owner"),
                                    ("Manager", "Manager"),
                                    ("Receptionist", "Receptionist"),
                                    ], 
                            default="Guest"
                            )
    picture	= models.ImageField(upload_to='profile_pics/')
    gender = models.CharField(choices=[
                                    ("Male", "Male"),
                                    ("Female", "Female")
                                    ], 
                            default="Male"
                            )
    nationality	= models.CharField(max_length=20, default="Ethiopian")
    hotel = models.ForeignKey('hotel.Hotel', on_delete=models.CASCADE, null=True, blank=True, related_name="staff_members")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD='email'

    objects = UserManager()
    

    class Meta:
        ordering = ["first_name"]

    def __str__(self):
        return f"Email: {self.email} -id: {self.id} "
    
    def is_hotel_staff(self):
        return self.role in ["Manager", "Receptionist"]
    
