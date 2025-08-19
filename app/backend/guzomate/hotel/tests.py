from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from accounts.models import User
from hotel.models import Hotel, Location, Room, Event, Amenities, Image
from django.core.files.uploadedfile import SimpleUploadedFile

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class HotelViewsTest(APITestCase):
    def setUp(self):
        # Create users with roles
        self.admin_user = User.objects.create_user(
            email="admin@example.com",
            first_name="Admin",
            last_name="User",
            phone="0900000000",
            gender="Male",
            role="Admin",
            nationality="Ethiopian",
            password="adminpass"
        )

        self.owner_user = User.objects.create_user(
            email="owner@example.com",
            first_name="Hotel",
            last_name="Owner",
            phone="0900000002",
            gender="Male",
            role="Owner",
            nationality="Ethiopian",
            password="ownerpass"
        )

        self.normal_user = User.objects.create_user(
            email="user@example.com",
            first_name="Normal",
            last_name="User",
            phone="0900000001",
            gender="Male",
            role="User",
            nationality="Ethiopian",
            password="userpass"
        )

        # Tokens
        self.admin_tokens = get_tokens_for_user(self.admin_user)
        self.owner_tokens = get_tokens_for_user(self.owner_user)
        self.user_tokens = get_tokens_for_user(self.normal_user)

        self.location = Location.objects.create(
            latitude=9.0, longitude=38.7, local_name="Addis Ababa"
        )
        self.hotel = Hotel.objects.create(
            owner=self.owner_user.id,
            name="Test Hotel",
            star=4,
            location=self.location
        )
        self.room = Room.objects.create(
            hotel=self.hotel, description="Deluxe Room", type="Deluxe",
            room_no="101", price_per_night=100.0, available=True, number_of_beds=2
        )

        self.manager_user = User.objects.create_user(
            email="manager@example.com",
            first_name="Hotel",
            last_name="Manager",
            phone="0900000003",
            gender="Male",
            role="Manager",
            hotel = self.hotel,
            nationality="Ethiopian",
            password="managerpass"
        )

        self.receptionist_user = User.objects.create_user(
            email="reception@example.com",
            first_name="Hotel",
            last_name="Receptionist",
            phone="0900000004",
            gender="Female",
            role="Receptionist",
            hotel = self.hotel,
            nationality="Ethiopian",
            password="receptionpass"
        )
        ##Token
        self.manager_tokens = get_tokens_for_user(self.manager_user)
        self.reception_tokens = get_tokens_for_user(self.receptionist_user)

        self.event1 = Event.objects.create(
            hotel=self.hotel,
            title="Event 1",
            description="First Event",
            accessibility="Free",
            price=50
        )
        self.event2 = Event.objects.create(
            hotel=self.hotel,
            title="Event 2",
            description="Second Event",
            accessibility="Paid",
            price=100
        )

        self.event3 = Event.objects.create(
            hotel=self.hotel,
            title="Event 3",
            description="Second Event",
            accessibility="Paid",
            price=100
        )

        self.amenity1 = Amenities.objects.create(
            hotel=self.hotel, name="WiFi", description="Free WiFi", availability=True, amenityable_type="Hotel"
        )
        self.amenity2 = Amenities.objects.create(
            hotel=self.hotel, name="Pool", description="Swimming Pool", availability=False, amenityable_type="Hotel"
        )


        # Room Amenities
        self.room_amenity1 = Amenities.objects.create(
            hotel=self.hotel, name="WiFi", description="Free WiFi", availability=True,
            amenityable_type="Room", amenityable_id=self.room
        )
        self.room_amenity2 = Amenities.objects.create(
            hotel=self.hotel, name="TV", description="Smart TV", availability=False,
            amenityable_type="Room", amenityable_id=self.room
        )

        ## Hotel image
        self.image_file = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        self.image1 = Image.objects.create(
            hotel=self.hotel.id, image=self.image_file, imageable_type="Hotel",
            imageable_id=self.hotel.id, hotel_name=self.hotel.name
        )
        self.image2 = Image.objects.create(
            hotel=self.hotel.id, image=self.image_file, imageable_type="Hotel",
            imageable_id=self.hotel.id, hotel_name=self.hotel.name
        )
        ## Room image
        self.Room_image = Image.objects.create(
            image=self.image_file, imageable_type="Room",
            imageable_id=self.room.id, hotel=self.hotel.id, hotel_name=self.hotel.name
        )
        self.Room_image2 = Image.objects.create(
            image=self.image_file, imageable_type="Room",
            imageable_id=self.room.id, hotel=self.hotel.id, hotel_name=self.hotel.name
        )
        ## Event image
        self.event_image1 = Image.objects.create(
            imageable_type='Event',
            imageable_id=self.event1.id,
            hotel=self.hotel.id,
            hotel_name=self.hotel.name,
            image=SimpleUploadedFile(name='test.jpg', content=b'\x47\x49\x46\x38', content_type='image/gif')
        )

        self.event_image2 = Image.objects.create(
            imageable_type='Event',
            imageable_id=self.event1.id,
            hotel=self.hotel.id,
            hotel_name=self.hotel.name,
            image=SimpleUploadedFile(name='test.jpg', content=b'\x47\x49\x46\x38', content_type='image/gif')
        )

    def test_admin_can_create_hotel(self):
        url = reverse("create_hotel")
        data = {
            "owner": str(self.owner_user.id),
            "name": "Admin Created Hotel",
            "star": 5,
            "location": {
                "latitude": 8.9,
                "longitude": 38.8,
                "local_name": "Bole"
            }
        }
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_tokens['access']}")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_non_admin_cannot_create_hotel(self):
        url = reverse("create_hotel")
        data = {
            "owner": str(self.normal_user.id),
            "name": "Blocked Hotel",
            "star": 3,
            "location": {
                "latitude": 7.0,
                "longitude": 39.0,
                "local_name": "Somewhere"
            }
        }
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_tokens['access']}")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_hotels(self):
        url = reverse("list_hotels")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_hotel(self):
        url = reverse("retrieve_hotel", kwargs={"hotel_id": str(self.hotel.id)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(self.hotel.id))

    def test_admin_can_update_hotel(self):
        url = reverse("update_hotel", kwargs={"hotel_id": str(self.hotel.id)})
        data = {
            "owner": str(self.owner_user.id),
            "name": "Updated Hotel Name",
            "star": 3,
            "location": {
                "latitude": 9.1,
                "longitude": 38.6,
                "local_name": "New Location"
            }
        }
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_tokens['access']}")
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.hotel.refresh_from_db()
        self.assertEqual(self.hotel.name, "Updated Hotel Name")

    def test_non_admin_cannot_update_hotel(self):
        url = reverse("update_hotel", kwargs={"hotel_id": str(self.hotel.id)})
        data = {
            "owner": str(self.owner_user.id),
            "name": "Blocked Update",
            "star": 2,
            "location": {
                "latitude": 7.5,
                "longitude": 39.5,
                "local_name": "BlockedLoc"
            }
        }
        for tokens in [self.owner_tokens, self.manager_tokens, self.reception_tokens, self.user_tokens]:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
            response = self.client.put(url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_delete_hotel(self):
        url = reverse("delete_hotel", kwargs={"hotel_id": str(self.hotel.id)})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_tokens['access']}")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_non_admin_cannot_delete_hotel(self):
        url = reverse("delete_hotel", kwargs={"hotel_id": str(self.hotel.id)})
        for tokens in [self.owner_tokens, self.manager_tokens, self.reception_tokens, self.user_tokens]:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_cannot_create_update_delete(self):
        create_url = reverse("create_hotel")
        update_url = reverse("update_hotel", kwargs={"hotel_id": str(self.hotel.id)})
        delete_url = reverse("delete_hotel", kwargs={"hotel_id": str(self.hotel.id)})

        # Try create
        response = self.client.post(create_url, {
            "owner": str(self.owner_user.id),
            "name": "Unauth Hotel",
            "star": 2,
            "location": {"latitude": 8.1, "longitude": 38.5, "local_name": "UnauthLoc"}
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Try update
        response = self.client.put(update_url, {
            "owner": str(self.owner_user.id),
            "name": "Unauth Update",
            "star": 3,
            "location": {"latitude": 7.2, "longitude": 37.9, "local_name": "NoAuthUpdate"}
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Try delete
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_hotel_with_invalid_data(self):
        """Admin tries to create hotel with missing fields → 400"""
        url = reverse("create_hotel")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_tokens['access']}")
        data = {"name": ""}  # Missing star, location, and invalid name
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_hotel_with_invalid_data(self):
        """Admin tries to update hotel with bad data → 400"""
        url = reverse("update_hotel", kwargs={"hotel_id": str(self.hotel.id)})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_tokens['access']}")
        data = {
            "owner": str(self.owner_user.id),
            "name": "", 
            "star": -1,  
            "location": {"latitude": None, "longitude": None, "local_name": ""}
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_non_existing_hotel(self):
        """Deleting non-existing hotel should return 404"""
        url = reverse("delete_hotel", kwargs={"hotel_id": "00000000-0000-0000-0000-000000000000"})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_tokens['access']}")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_non_existing_hotel(self):
        """Retrieving non-existing hotel should return 404"""
        url = reverse("retrieve_hotel", kwargs={"hotel_id": "00000000-0000-0000-0000-000000000000"})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_tokens['access']}")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

##Room
    def test_owner_can_create_room(self):
        url = reverse("create_room", kwargs={"hotel_id": str(self.hotel.id)})
        data = {
            "description": "New Room",
            "type": "Suite",
            "room_no": "102",
            "price_per_night": 200.0,
            "available": True,
            "number_of_beds": 1
        }
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.owner_tokens['access']}")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_manager_can_create_room(self):
        url = reverse("create_room", kwargs={"hotel_id": str(self.hotel.id)})
        data = {
            "description": "Manager Room",
            "type": "Standard",
            "room_no": "103",
            "price_per_night": 150.0,
            "available": True,
            "number_of_beds": 2
        }
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.manager_tokens['access']}")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_receptionist_and_user_cannot_create_room(self):
        url = reverse("create_room", kwargs={"hotel_id": str(self.hotel.id)})
        data = {
            "description": "Unauthorized Room",
            "type": "Standard",
            "room_no": "104",
            "price_per_night": 120.0,
            "available": True,
            "number_of_beds": 1
        }
        for tokens in [self.reception_tokens, self.user_tokens, self.admin_tokens]:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
            response = self.client.post(url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_update_room(self):
        url = reverse("update_room", kwargs={"hotel_id": str(self.hotel.id), "room_id": str(self.room.id)})
        data = {
            "description": "Updated by Owner",
            "type": "Deluxe",
            "room_no": "201",
            "price_per_night": 180.0,
            "available": False,
            "number_of_beds": 2
        }
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.owner_tokens['access']}")
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_manager_can_update_room(self):
        url = reverse("update_room", kwargs={"hotel_id": str(self.hotel.id), "room_id": str(self.room.id)})
        data = {
            "description": "Updated by Manager",
            "type": "Standard",
            "room_no": "202",
            "price_per_night": 170.0,
            "available": True,
            "number_of_beds": 1
        }
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.manager_tokens['access']}")
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_receptionist_can_update_room(self):
        url = reverse("update_room", kwargs={"hotel_id": str(self.hotel.id), "room_id": str(self.room.id)})
        data = {
            "price_per_night": 120.0,
            "available": False
        }

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.reception_tokens['access']}")
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        room = Room.objects.get(id=self.room.id)
        self.assertEqual(room.price_per_night, 120.0)
        self.assertEqual(room.available, False)

    def test_user_cannot_update_room(self):
        url = reverse("update_room", kwargs={"hotel_id": str(self.hotel.id), "room_id": str(self.room.id)})
        data = {
            "description": "Invalid Update",
            "type": "Suite",
            "room_no": "203",
            "price_per_night": 250.0,
            "available": True,
            "number_of_beds": 2
        }
        for tokens in [self.user_tokens, self.admin_tokens]:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
            response = self.client.put(url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_delete_room(self):
        url = reverse("delete_room", kwargs={"hotel_id": str(self.hotel.id), "room_id": str(self.room.id)})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.owner_tokens['access']}")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_manager_can_delete_room(self):
        url = reverse("delete_room", kwargs={"hotel_id": str(self.hotel.id), "room_id": str(self.room.id)})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.manager_tokens['access']}")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_receptionist_and_user_cannot_delete_room(self):
        url = reverse("delete_room", kwargs={"hotel_id": str(self.hotel.id), "room_id": str(self.room.id)})
        for tokens in [self.reception_tokens, self.user_tokens, self.admin_tokens]:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_and_retrieve_rooms_allowed_for_all(self):
        list_url = reverse("list_rooms", kwargs={"hotel_id": str(self.hotel.id)})
        detail_url = reverse("retrieve_room", kwargs={"hotel_id": str(self.hotel.id), "room_id": str(self.room.id)})

        for tokens in [self.admin_tokens, self.owner_tokens, self.manager_tokens, self.reception_tokens, self.user_tokens]:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
            self.assertEqual(self.client.get(list_url).status_code, status.HTTP_200_OK)
            self.assertEqual(self.client.get(detail_url).status_code, status.HTTP_200_OK)

    def test_create_room_with_invalid_data(self):
        url = reverse("create_room", kwargs={"hotel_id": str(self.hotel.id)})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.owner_tokens['access']}")
        data = {
            "description": "",
            "type": "",
            "room_no": "",
            "price_per_night": -50,  
            "available": True,
            "number_of_beds": -1 
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_non_existing_room(self):
        url = reverse("update_room", kwargs={"hotel_id": str(self.hotel.id), "room_id": "00000000-0000-0000-0000-000000000000"})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.owner_tokens['access']}")
        data = {
            "description": "Update Non Existing",
            "type": "Standard",
            "room_no": "300",
            "price_per_night": 120.0,
            "available": True,
            "number_of_beds": 2
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_non_existing_room(self):
        url = reverse("delete_room", kwargs={"hotel_id": str(self.hotel.id), "room_id": "00000000-0000-0000-0000-000000000000"})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.owner_tokens['access']}")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

## Staff
    def test_manager_can_create_receptionist(self):
        create_url = reverse('create_staff', kwargs={'hotel_id': self.hotel.id})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.manager_tokens['access']}")
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "phone": "0910000009",
            "password": "John123!",
            "role": "Receptionist"
        }
        response = self.client.post(create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(email="john@example.com").exists(), True)

    def test_receptionist_can_be_updated_by_manager(self):
        create_url = reverse('create_staff', kwargs={'hotel_id': self.hotel.id})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.manager_tokens['access']}")
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "phone": "0910000009",
            "password": "John123!",
            "role": "Receptionist"
        }
        response = self.client.post(create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(email="john@example.com").exists(), True)
        id = response.data.get('id')
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.manager_tokens['access']}")
        detail_url = reverse('retrieve_staff', kwargs={'hotel_id': self.hotel.id, 'staff_id': id})
        data = {
            "first_name": "Updated",
            "phone": "+251911223344"
        }
        response = self.client.patch(detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
        user = User.objects.get(email="john@example.com")
        self.assertEqual(user.first_name, "Updated")
        self.assertEqual(user.phone, "+251911223344")

    def test_owner_can_list_staff(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.owner_tokens['access']}", format="json")
        list_url = reverse('list_staff', kwargs={"hotel_id": self.hotel.id})
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_non_manager_cannot_update_staff(self):
        create_url = reverse('create_staff', kwargs={'hotel_id': self.hotel.id})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.manager_tokens['access']}")
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "phone": "0910000009",
            "password": "John123!",
            "role": "Receptionist"
        }
        response = self.client.post(create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(email="john@example.com").exists(), True)
        id = response.data.get('id')        

        non_manager = User.objects.create_user(
            email="other@example.com",
            password="Other123!",
            role="Receptionist"
        )
        detail_url = reverse('retrieve_staff', kwargs={"hotel_id": self.hotel.id, "staff_id": id})
        self.client.force_authenticate(user=non_manager)
        data = {"first_name": "Hack"}
        response = self.client.patch(detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

##Event
    def test_any_user_can_list_events(self):
        url = reverse("list_events", kwargs={"hotel_id": self.hotel.id})
        for tokens in [self.admin_tokens, self.owner_tokens, self.manager_tokens,
                       self.reception_tokens, self.user_tokens]:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = response.data
            event_ids = [event["id"] for event in data.get("results", [])]
            self.assertIn(str(self.event1.id), event_ids)
            self.assertIn(str(self.event2.id), event_ids)

    def test_any_user_can_retrieve_event(self):
        url = reverse("retrieve_event", kwargs={"hotel_id": self.hotel.id, "event_id": self.event1.id})
        for tokens in [self.admin_tokens, self.owner_tokens, self.manager_tokens,
                       self.reception_tokens, self.user_tokens]:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["id"], str(self.event1.id))

    def test_owner_and_manager_can_create_event(self):
        url = reverse("create_event", kwargs={"hotel_id": self.hotel.id})
        data = {
            "title": "New Event",
            "description": "Created by test",
            "accessibility": "Paid",
            "price": 75
        }
        for tokens in [self.owner_tokens, self.manager_tokens]:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
            response = self.client.post(url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_any_user_can_not_create_event(self):
        url = reverse("create_event", kwargs={"hotel_id": self.hotel.id})
        data = {
            "title": "New Event",
            "description": "Created by test",
            "accessibility": "Paid",
            "price": 75
        }
        for tokens in [self.admin_tokens, self.reception_tokens, self.user_tokens]:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
            response = self.client.post(url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_and_manager_can_update_event(self):
        url = reverse("update_event", kwargs={"hotel_id": self.hotel.id, "event_id": self.event1.id})
        data = {
            "title": "Updated Event",
            "description": "Updated description",
            "accessibility": "Paid",
            "price": 80
        }
        for tokens in [self.owner_tokens, self.manager_tokens]:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
            response = self.client.put(url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['title'], "Updated Event")

    def test_admin_user_and_receptionist_can_not_update_event(self):
        url = reverse("update_event", kwargs={"hotel_id": self.hotel.id, "event_id": self.event1.id})
        data = {
            "title": "invalid update Event",
            "description": "Updated description",
            "accessibility": "Paid",
            "price": 80
        }
        for tokens in [self.admin_tokens, self.reception_tokens, self.user_tokens]:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
            response = self.client.put(url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(response.data['detail'].code, "permission_denied")
    
    def test_admin_user_and_receptionist_can_not_delete_event(self):
        url = reverse("delete_event", kwargs={"hotel_id": self.hotel.id, "event_id": self.event2.id})
        for tokens in [self.admin_tokens, self.reception_tokens, self.user_tokens]:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_and_manager_can_delete_event(self):
        events = [self.event1, self.event2]  # one for manager, one for owner
        users_tokens = [self.manager_tokens, self.owner_tokens]

        for event, tokens in zip(events, users_tokens):
            url = reverse("delete_event", kwargs={"hotel_id": self.hotel.id, "event_id": event.id})
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

##Amenities
    def test_any_user_can_list_amenities(self):
        url = reverse("list_amenities", kwargs={"hotel_id": self.hotel.id})
        for tokens in [self.admin_tokens, self.owner_tokens, self.manager_tokens,
                       self.reception_tokens, self.user_tokens]:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            amenity_ids = [a["id"] for a in response.data['results']]
            self.assertIn(str(self.amenity1.id), amenity_ids)
            self.assertIn(str(self.amenity2.id), amenity_ids)

    def test_any_user_can_retrieve_amenity(self):
        url = reverse("retrieve_amenity", kwargs={"hotel_id": self.hotel.id, "amenity_id": self.amenity1.id})
        for tokens in [self.admin_tokens, self.owner_tokens, self.manager_tokens,
                       self.reception_tokens, self.user_tokens]:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["id"], str(self.amenity1.id))
    
    def test_any_owner_and_manager_can_create_amenity(self):
        url = reverse("create_amenity", kwargs={"hotel_id": self.hotel.id})
        data = {"name": "Gym", "description": "Fitness Center", "availability": True}
        for tokens in [self.manager_tokens, self.owner_tokens]:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
            response = self.client.post(url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_any_user_can_not_create_amenity(self):
        url = reverse("create_amenity", kwargs={"hotel_id": self.hotel.id})
        data = {"name": "Gym", "description": "Fitness Center", "availability": True}
        for tokens in [self.admin_tokens, self.reception_tokens, self.user_tokens]:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
            response = self.client.post(url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_any_owner_and_manager_can_update_amenity(self):
        url = reverse("update_amenity", kwargs={"hotel_id": self.hotel.id, "amenity_id": self.amenity1.id})
        data = {"name": "WiFi Updated", "description": "Updated Desc", "availability": False}
        for tokens in [self.owner_tokens, self.manager_tokens]:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
            response = self.client.put(url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["name"], "WiFi Updated")

    def test_any_user_can_not_update_amenity(self):
        url = reverse("update_amenity", kwargs={"hotel_id": self.hotel.id, "amenity_id": self.amenity1.id})
        data = {"name": "WiFi Updated", "description": "Updated Desc", "availability": False}
        for tokens in [self.admin_tokens, self.reception_tokens, self.user_tokens]:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
            response = self.client.put(url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_and_manager_can_delete_amenity(self):
        amenities = [self.amenity1, self.amenity2]  
        users_tokens = [self.manager_tokens, self.owner_tokens]
        for amenity, tokens in zip(amenities, users_tokens):
            url = reverse("delete_amenity", kwargs={"hotel_id": self.hotel.id, "amenity_id": amenity.id})
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_any_user_can_not_delete_amenity(self):
        url = reverse("delete_amenity", kwargs={"hotel_id": self.hotel.id, "amenity_id": self.amenity2.id})
        for tokens in [self.admin_tokens, self.reception_tokens, self.user_tokens]:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

##Room amenity
    def test_any_user_can_list_room_amenities(self):
        url = reverse("list_room_amenities", kwargs={"hotel_id": self.hotel.id, "room_id": self.room.id})
        for tokens in [self.admin_tokens, self.owner_tokens, self.manager_tokens,
                       self.reception_tokens, self.user_tokens]:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            amenity_ids = [a["id"] for a in response.data['results']]
            self.assertIn(str(self.room_amenity1.id), amenity_ids)
            self.assertIn(str(self.room_amenity2.id), amenity_ids)

    def test_any_user_can_retrieve_room_amenity(self):
        url = reverse("retrieve_room_amenity", kwargs={
            "hotel_id": self.hotel.id, "room_id": self.room.id, "amenity_id": self.room_amenity1.id
        })
        for tokens in [self.admin_tokens, self.owner_tokens, self.manager_tokens,
                       self.reception_tokens, self.user_tokens]:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["id"], str(self.room_amenity1.id))

    def test_manager_and_owner_can_create_room_amenity(self):
        url = reverse("create_room_amenity", kwargs={"hotel_id": self.hotel.id, "room_id": self.room.id})
        data = {"name": "Mini Bar", "description": "Available drinks", "availability": True}
        for tokens in [self.owner_tokens, self.manager_tokens]:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
            response = self.client.post(url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data["name"], "Mini Bar")

    def test_any_user_can_not_create_room_amenity(self):
        url = reverse("create_room_amenity", kwargs={"hotel_id": self.hotel.id, "room_id": self.room.id})
        data = {"name": "Mini Bar", "description": "Available drinks", "availability": True}
        for tokens in [self.admin_tokens, self.reception_tokens, self.user_tokens]:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
            response = self.client.post(url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(response.data["detail"], "You do not have permission to perform this action.")

    def test_manager_and_owner_update_room_amenity(self):
        url = reverse("update_room_amenity", kwargs={
            "hotel_id": self.hotel.id, "room_id": self.room.id, "amenity_id": self.room_amenity1.id
        })
        data = {"name": "WiFi Updated", "description": "Updated Desc", "availability": False}
        for tokens in [self.owner_tokens, self.manager_tokens]:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
            response = self.client.put(url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["name"], "WiFi Updated")

    def test_any_user_can_not_update_room_amenity(self):
        url = reverse("update_room_amenity", kwargs={
            "hotel_id": self.hotel.id, "room_id": self.room.id, "amenity_id": self.room_amenity1.id
        })
        data = {"name": "WiFi Updated", "description": "Updated Desc", "availability": False}
        for tokens in [self.admin_tokens, self.reception_tokens, self.user_tokens]:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
            response = self.client.put(url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(response.data["detail"], "You do not have permission to perform this action.")

    def test_manager_and_owner_can_delete_room_amenity(self):
        amenities = [self.room_amenity1.id, self.room_amenity2.id]  
        users_tokens = [self.manager_tokens, self.owner_tokens]

        for amenity, tokens in zip(amenities, users_tokens):
            url = reverse("delete_room_amenity", kwargs={"hotel_id": self.hotel.id, "room_id": self.room.id, "amenity_id": amenity})
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_any_user_can_not_delete_room_amenity(self):
        amenities = [self.room_amenity1.id, self.room_amenity2.id]  
        users_tokens = [self.admin_tokens, self.reception_tokens, self.user_tokens]

        for amenity, tokens in zip(amenities, users_tokens):
            url = reverse("delete_room_amenity", kwargs={"hotel_id": self.hotel.id, "room_id": self.room.id, "amenity_id": amenity})
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


## Hotel image
    def test_non_owner_manager_cannot_create_hotel_image(self):
        url = reverse(
            "create_hotel_image",
            kwargs={"hotel_id": self.hotel.id}
        )
        data = {
            'imageable_type': 'Hotel',
            'image': SimpleUploadedFile(
                name='new_test_hotel.jpg',
                content=b'\x47\x49\x46\x38',
                content_type='image/gif'
            )
        }
        for tokens in [self.reception_tokens, self.user_tokens]:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
            response = self.client.post(url, data, format="multipart")
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_any_user_can_list_hotel_images(self):
        url = reverse("list_hotel_images", kwargs={"hotel_id": self.hotel.id})
        for tokens in [self.admin_tokens, self.owner_tokens, self.manager_tokens,
                       self.reception_tokens, self.user_tokens]:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_any_user_can_retrieve_hotel_image(self):
        url = reverse("retrieve_hotel_image", kwargs={"hotel_id": self.hotel.id, "image_id": self.image1.id})
        for tokens in [self.admin_tokens, self.owner_tokens, self.manager_tokens,
                       self.reception_tokens, self.user_tokens]:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["id"], str(self.image1.id))

    def test_any_user_can_not_create_hotel_image_with_invalid_image(self):
        url = reverse("create_hotel_image", kwargs={"hotel_id": self.hotel.id})
        data = {
            'imageable_type': 'Hotel',
            'image': SimpleUploadedFile(
                name='test_image.jpg',
                content=b'test_file_content',
                content_type='image/jpeg'
            )
        }

        for tokens in [self.owner_tokens, self.manager_tokens]:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
            response = self.client.post(url, data, format="multipart")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_only_owner_manager_can_delete_hotel_image(self):
        images = [self.image1.id, self.image2.id]  
        users_tokens = [self.manager_tokens, self.owner_tokens]
        url = reverse("delete_hotel_image", kwargs={"hotel_id": self.hotel.id, "image_id": self.image1.id})

        for image, token in zip(images, users_tokens):
            url = reverse("delete_hotel_image", kwargs={"hotel_id": self.hotel.id, "image_id": image})
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_any_user_can_not_delete_hotel_image(self):
        images = [self.image1.id, self.image2.id]  
        users_tokens = [self.admin_tokens, self.reception_tokens, self.user_tokens]
        url = reverse("delete_hotel_image", kwargs={"hotel_id": self.hotel.id, "image_id": self.image1.id})

        for image, token in zip(images, users_tokens):
            url = reverse("delete_hotel_image", kwargs={"hotel_id": self.hotel.id, "image_id": image})
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")
            response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

## Room Image
    def test_non_owner_manager_cannot_create_room_image(self):
        url = reverse(
            "create_room_image",
            kwargs={"hotel_id": self.hotel.id, "room_id": self.room.id}
        )
        data = {
            'image': SimpleUploadedFile(
                name='new_test_room.jpg',
                content=b'\x47\x49\x46\x38',
                content_type='image/gif'
            )
        }

        for tokens in [self.reception_tokens, self.user_tokens]:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
            response = self.client.post(url, data, format="multipart")
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_any_user_can_list_room_images(self):
        url = reverse("list_room_images", kwargs={"hotel_id": self.hotel.id, "room_id": self.room.id})
        for tokens in [self.admin_tokens, self.owner_tokens, self.manager_tokens,
                       self.reception_tokens, self.user_tokens]:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['results'][0]['id'], str(self.Room_image.id))

    def test_any_user_can_retrieve_room_image(self):
        url = reverse("retrieve_room_image", kwargs={"hotel_id": self.hotel.id, "room_id": self.room.id, "image_id": self.Room_image.id})
        for tokens in [self.admin_tokens, self.owner_tokens, self.manager_tokens,
                       self.reception_tokens, self.user_tokens]:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["id"], str(self.Room_image.id))

    def test_only_owner_manager_can_delete_room_image(self):
        images = [self.Room_image.id, self.Room_image2.id]  
        users_tokens = [self.manager_tokens, self.owner_tokens]
        
        for image, token in zip(images, users_tokens):
            url = reverse("delete_room_image", kwargs={"hotel_id": self.hotel.id, "room_id": self.room.id, "image_id": image})
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_any_user_cannot_delete_room_image(self):
        url = reverse("delete_room_image", kwargs={"hotel_id": self.hotel.id, "room_id": self.room.id, "image_id": self.Room_image.id})
        for tokens in [self.admin_tokens, self.reception_tokens, self.user_tokens]:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

## Event image
    def test_any_user_can_list_event_images(self):
        url = reverse("list_event_images", kwargs={"hotel_id": self.hotel.id, "event_id": self.event1.id})
        for tokens in [self.owner_tokens, self.manager_tokens, self.reception_tokens, self.user_tokens]:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(len(response.data) >= 2)
    
    def test_any_user_can_retrieve_event_image(self):
        url = reverse("retrieve_event_image", kwargs={"hotel_id": self.hotel.id, "event_id": self.event1.id, "image_id": self.event_image1.id})
        for tokens in [self.owner_tokens, self.manager_tokens, self.reception_tokens, self.user_tokens]:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["id"], str(self.event_image1.id))

    def test_non_owner_manager_cannot_create_event_image(self):
        url = reverse("create_event_image", kwargs={"hotel_id": self.hotel.id, "event_id": self.event1.id})
        data = {
            'image': SimpleUploadedFile(name='new_test.jpg', content=b'\x47\x49\x46\x38', content_type='image/gif')
        }

        for tokens in [self.reception_tokens, self.user_tokens]:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
            response = self.client.post(url, data, format="multipart")
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_only_owner_manager_can_delete_event_image(self):
        images = [self.event_image1.id, self.event_image2.id]  
        users_tokens = [self.manager_tokens, self.owner_tokens]

        for image, token in zip(images, users_tokens):
            url = reverse(
                "delete_event_image",
                kwargs={"hotel_id": self.hotel.id, "event_id": self.event1.id, "image_id": image}
            )
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_non_owner_manager_cannot_delete_event_image(self):
        images = [self.event_image1.id, self.event_image2.id]  
        users_tokens = [self.reception_tokens, self.user_tokens]

        for image, token in zip(images, users_tokens):
            url = reverse(
                "delete_event_image",
                kwargs={"hotel_id": self.hotel.id, "event_id": self.event1.id, "image_id": image}
            )
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)