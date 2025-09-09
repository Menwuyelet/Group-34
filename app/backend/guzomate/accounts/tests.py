# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from hotel.models import Hotel, Room, Location
from business.models import Booking, UserHistory, Favorite
from datetime import date, timedelta

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserViewsTest(APITestCase):

    def setUp(self):
        # Create users with different roles
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

        self.test_user = User.objects.create_user(
            email="test@gmail.com",
            first_name="test",
            last_name="test",
            phone="0900000001",
            gender="Male",
            nationality="Ethiopian",
            password="normaluser"
        )
        self.test_user1 = User.objects.create_user(
            email="test1@gmail.com",
            first_name="test",
            last_name="test",
            phone="09000000009",
            gender="Male",
            nationality="Ethiopian",
            password="normaluser"
        )
        url_auth = reverse('token_obtain_pair')
        admin_creds = {
            "email": "admin@example.com",
            "password": "adminpass"
        }
        response = self.client.post(url_auth, admin_creds, format='json')
        self.admin_token = response.data['access']

        guest_creds = {
            "email": "test@gmail.com",
            "password": "normaluser"
        }
        response = self.client.post(url_auth, guest_creds, format='json')
        self.guest_token = response.data['access']
        test_user_cred = {
            "email": "test1@gmail.com",
            "password": "normaluser"
        }
        response = self.client.post(url_auth, test_user_cred, format='json')
        self.test_user_token = response.data['access']
        
        ##Booking
        self.owner_user = User.objects.create_user(
            email="owner001@example.com",
            first_name="Hotel",
            last_name="Owner",
            phone="0900000002",
            gender="Male",
            role="Owner",
            nationality="Ethiopian",
            password="ownerpass"
        )
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

        self.valid_payload = {
            "number_of_adults": 2,
            "number_of_children": 1,
            "start_date": str(date.today()),
            "end_date": str(date.today() + timedelta(days=3)),
            "total_price": 300,
        }

        self.booking = Booking.objects.create(
            user=self.test_user,
            hotel=self.hotel,
            room=self.room,
            guest_name="John Doe",
            guest_phone="+251900000001",
            guest_nationality="Ethiopian",
            guest_gender="Male",
            number_of_adults=2,
            number_of_children=1,
            start_date=str(date.today() + timedelta(days=4)),
            end_date=str(date.today() + timedelta(days=5)),
            booking_source="Online",
            status="Pending",
            total_price=100
        )

        ## Payload to update booking
        self.update_payload = {
            "number_of_adults": 3,
            "number_of_children": 0,
            "guest_name": "John Updated",
            "guest_phone": "+251911111111",
        }

        self.booking1 = Booking.objects.create(
            user=self.test_user,
            hotel=self.hotel,
            room=self.room,
            guest_name="John Doe",
            guest_phone="+251900000001",
            guest_nationality="Ethiopian",
            guest_gender="Male",
            number_of_adults=2,
            number_of_children=1,
            start_date=str(date.today() + timedelta(days=6)),
            end_date=str(date.today() + timedelta(days=7)),
            booking_source="Online",
            status="Pending",
            total_price=100
        )

        self.other_booking = Booking.objects.create(
            user=self.admin_user,
            hotel=self.hotel,
            room=self.room,
            guest_name="Other User",
            guest_phone="+251922222222",
            guest_nationality="Ethiopian",
            guest_gender="Male",
            number_of_adults=1,
            number_of_children=0,
            start_date=str(date.today() + timedelta(days=8)),
            end_date=str(date.today() + timedelta(days=9)),
            booking_source="Online",
            status="Pending",
            total_price=100
        )

        self.user_history1 = UserHistory.objects.create(
            user=self.test_user,
            booking=self.booking,
        )
        self.user_history2 = UserHistory.objects.create(
            user=self.test_user,
            booking=self.booking1
        )

        ## Another user's history 
        self.other_user_history = UserHistory.objects.create(
            user=self.admin_user,
            booking=self.other_booking
        )

        ## Favorite
        self.favorite = Favorite.objects.create(
            user=self.test_user,
            hotel=self.hotel.id
        )
    ## user
    def test_create_user_with_valid_data(self):
        url = reverse('create_user')
        data = {
            "email": "newuser1@example.com",
            "first_name": "New",
            "last_name": "User",
            "phone": "09000000011",
            "password": "newuserpass1@"
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_with_faulty_password(self):
        url = reverse('create_user')
        data = {
            "email": "newuser1@example.com",
            "first_name": "New",
            "last_name": "User",
            "phone": "09000000011",
            "password": "newuserpass"
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.filter(role='Guest').count(), 2)

    def test_guest_auth(self):
        url = reverse('token_obtain_pair')
        data = {
            "email": "test@gmail.com",
            "password": "normaluser"
        }

        ## with valid data
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ## with invalid credential
        data['password'] = "12345689"
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_listing_guests(self):
        url_auth = reverse('token_obtain_pair')
        data = {
            "email": "test@gmail.com",
            "password": "normaluser"
        }
        response = self.client.post(url_auth, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        ## test listing with unauthorized user
        url_listing = reverse('list_users')
        guest_token = response.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {guest_token}')
        response = self.client.post(url_listing)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        ## test listing with authorized user
        data = {
            "email": "admin@example.com",
            "password": "adminpass"
        }
        response = self.client.post(url_auth, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        admin_token = response.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')
        response = self.client.get(url_listing)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_getting_guest_detail(self):
        url_auth = reverse('token_obtain_pair')
        guest_creds = {
            "email": "test1@gmail.com",
            "password": "normaluser"
        }
        response = self.client.post(url_auth, guest_creds, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        guest_token = response.data['access']
        guest_id = response.data['user']['id']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {guest_token}')

        url_detail = reverse('retrieve_user', kwargs={"id": guest_id})
        response = self.client.get(url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], guest_creds["email"])
        
        ## update user with self
        update_data = {
            "email": "test2@gmail.com",
            "password": "normaluser1@"
        }
        response = self.client.patch(url_detail, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], update_data["email"])

        ## delete user with self
        response = self.client.delete(url_detail, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_getting_user_detail_with_admin(self):
        url_auth = reverse('token_obtain_pair')
        guest_creds = {
            "email": "test1@gmail.com",
            "password": "normaluser"
        }
        response = self.client.post(url_auth, guest_creds, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        guest_id = response.data['user']['id']
    
        admin_creds = {
            "email": "admin@example.com",
            "password": "adminpass"
        }
        response = self.client.post(url_auth, admin_creds, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        admin_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        ## get detail
        url_detail = reverse('retrieve_user', kwargs={"id": guest_id})
        response = self.client.get(url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], guest_creds["email"])
        url_detail = reverse('retrieve_user', kwargs={'id': guest_id})
        
        ## update user
        update_data = {
            "email": "test2@gmail.com",
            "password": "normaluser1@"
        }
        response = self.client.patch(url_detail, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], update_data["email"])

        ## delete user
        response = self.client.delete(url_detail, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_getting_guest_detail_with_unauthorized_user(self):
        url_auth = reverse('token_obtain_pair')
        
        data = {
            "email": "admin@example.com",
            "password": "adminpass"
        }
        response = self.client.post(url_auth, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        admin_id= response.data['user']['id']
        url_detail = reverse('retrieve_user', kwargs={'id': admin_id})

        guest_creds = {
            "email": "test@gmail.com",
            "password": "normaluser"
        }
        response = self.client.post(url_auth, guest_creds, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        guest_token = response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {guest_token}')
        response = self.client.get(url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        url_update = reverse('retrieve_user', kwargs={"id": admin_id})
        update_data = {
            "email": "admin1@gmail.com"
        }

        response = self.client.patch(url_update, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    ## admin
    def test_admin_creation_with_admin(self):
        url_auth = reverse('token_obtain_pair')
        admin_creds = {
            "email": "admin@example.com",
            "password": "adminpass"
        }
        response = self.client.post(url_auth, admin_creds, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        admin_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        admin_url = reverse('admins-list')
        admin_data = {
            "email": "admintest@example.com",
            "first_name": "Admin",
            "last_name": "User",
            "phone": "0910000000",
            "gender": "Male",
            "nationality": "Ethiopian",
            "password": "admintestpass@1"
        }

        response = self.client.post(admin_url, admin_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], admin_data['email'])
        self.assertEqual(response.data['role'], "Admin")

    def test_admin_creation_with_faulty_creds(self):
        url_auth = reverse('token_obtain_pair')
        admin_creds = {
            "email": "admin@example.com",
            "password": "adminpass"
        }
        response = self.client.post(url_auth, admin_creds, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        admin_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')
        
        ## invalid data
        admin_url = reverse('admins-list')
        admin_data = {
            "email": "admintest@example.com",
            "first_name": "Admin",
            "last_name": "User",
            "phone": "0910000000",
            "gender": "Male",
            "nationality": "Ethiopian",
            "password": "admintestpas"
        }

        response = self.client.post(admin_url, admin_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


        ## un authorized User
        url_auth = reverse('token_obtain_pair')
        guest_creds = {
            "email": "test@gmail.com",
            "password": "normaluser"
        }
        response = self.client.post(url_auth, guest_creds, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        guest_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {guest_token}')

        admin_data = {
            "email": "admintest1@example.com",
            "first_name": "Admin",
            "last_name": "User",
            "phone": "0920000000",
            "gender": "Male",
            "nationality": "Ethiopian",
            "password": "admintestpas@1"
        }

        response = self.client.post(admin_url, admin_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_retrive(self):
        url_auth = reverse('token_obtain_pair')
        admin_creds = {
            "email": "admin@example.com",
            "password": "adminpass"
        }
        response = self.client.post(url_auth, admin_creds, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        admin_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')
        
        admin_url = reverse('admins-list')
        ## valid user
        response = self.client.get(admin_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

        ## invalid user
        guest_creds = {
            "email": "test@gmail.com",
            "password": "normaluser"
        }
        response = self.client.post(url_auth, guest_creds, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        guest_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {guest_token}')
        response = self.client.get(admin_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    ## owner
    def test_admin_can_retrieve_owner(self):
        owner_data = {
            "email": "owner@example.com",
            "first_name": "owner",
            "last_name": "User",
            "phone": "0930000000",
            "gender": "Male",
            "nationality": "Ethiopian",
            "password": "admintestpas@1"
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        create_url = reverse('create_owner')
        response = self.client.post(create_url, owner_data, format='json')
        owner_id = response.data['id']

        retrieve_url = reverse('retrieve_owner', kwargs={'id': owner_id})
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], owner_data['email'])

    def test_admin_can_update_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        owner_data = {
            "email": "owner@example.com",
            "first_name": "owner",
            "last_name": "User",
            "phone": "0930000000",
            "gender": "Male",
            "nationality": "Ethiopian",
            "password": "admintestpas@1"
        }
        create_url = reverse('create_owner')
        response = self.client.post(create_url, owner_data, format='json')
        owner_id = response.data['id']

        retrieve_url = reverse('retrieve_owner', kwargs={'id': owner_id})
        update_data = {"first_name": "UpdatedOwner", "phone": "0930000001"}
        response = self.client.patch(retrieve_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        owner_obj = User.objects.get(id=owner_id)
        self.assertEqual(owner_obj.first_name, "UpdatedOwner")
        self.assertEqual(owner_obj.phone, "0930000001")

    def test_admin_can_list_owners(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        create_url = reverse('create_owner')
        owner_data = {
            "email": "owner@example.com",
            "first_name": "owner",
            "last_name": "User",
            "phone": "0930000000",
            "gender": "Male",
            "nationality": "Ethiopian",
            "password": "admintestpas@1"
        }
        self.client.post(create_url, owner_data, format='json')

        list_url = reverse('list_owners')
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data['count'], 1)

    def test_admin_can_delete_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        owner_data = {
            "email": "owner@example.com",
            "first_name": "owner",
            "last_name": "User",
            "phone": "0930000000",
            "gender": "Male",
            "nationality": "Ethiopian",
            "password": "admintestpas@1"
        }
        create_url = reverse('create_owner')
        response = self.client.post(create_url,owner_data, format='json')
        owner_id = response.data['id']

        retrieve_url = reverse('retrieve_owner', kwargs={'id': owner_id})
        response = self.client.delete(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=owner_id).exists())
    
    def test_unauthorized_user_cannot_create_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.guest_token}')
        owner_data = {
            "email": "owner@example.com",
            "first_name": "owner",
            "last_name": "User",
            "phone": "0930000000",
            "gender": "Male",
            "nationality": "Ethiopian",
            "password": "admintestpas@1"
        }
        create_url = reverse('create_owner')
        response = self.client.post(create_url, owner_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
 
    def test_unauthorized_user_cannot_retrieve_owner(self):
        # Create owner as admin
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        owner_data = {
            "email": "owner@example.com",
            "first_name": "owner",
            "last_name": "User",
            "phone": "0930000000",
            "gender": "Male",
            "nationality": "Ethiopian",
            "password": "admintestpas@1"
        }
        create_url = reverse('create_owner')
        response = self.client.post(create_url, owner_data, format='json')
        owner_id = response.data['id']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.guest_token}')
        retrieve_url = reverse('retrieve_owner', kwargs={'id': owner_id})
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_user_cannot_update_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        owner_data = {
            "email": "owner@example.com",
            "first_name": "owner",
            "last_name": "User",
            "phone": "0930000000",
            "gender": "Male",
            "nationality": "Ethiopian",
            "password": "admintestpas@1"
        }
        create_url = reverse('create_owner')
        response = self.client.post(create_url, owner_data, format='json')
        owner_id = response.data['id']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.guest_token}')
        retrieve_url = reverse('retrieve_owner', kwargs={'id': owner_id})
        response = self.client.patch(retrieve_url, {"first_name": "Hack"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_user_cannot_delete_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        owner_data = {
            "email": "owner@example.com",
            "first_name": "owner",
            "last_name": "User",
            "phone": "0930000000",
            "gender": "Male",
            "nationality": "Ethiopian",
            "password": "admintestpas@1"
        }        
        create_url = reverse('create_owner')
        response = self.client.post(create_url, owner_data, format='json')
        owner_id = response.data['id']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.guest_token}')
        retrieve_url = reverse('retrieve_owner', kwargs={'id': owner_id})
        response = self.client.delete(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_user_cannot_list_owners(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.guest_token}')
        list_url = reverse('list_owners')
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    ##Booking
    def test_create_booking_success(self):
        url = reverse(
            "book_online",
            kwargs={"hotel_id": self.hotel.id, "room_id": self.room.id},
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.guest_token}")
        response = self.client.post(url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 4)

        booking = Booking.objects.filter(start_date=str(date.today()))
        self.assertEqual(booking[0].user, self.test_user)
        self.assertEqual(booking[0].hotel, self.hotel)
        self.assertEqual(booking[0].room, self.room)
        self.assertEqual(booking[0].booking_source, "Online")

    def test_create_booking_invalid_dates(self):
        url = reverse(
            "book_online",
            kwargs={"hotel_id": self.hotel.id, "room_id": self.room.id},
        )        
        payload = self.valid_payload.copy()
        payload["end_date"] = str(date.today() - timedelta(days=1))

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.guest_token}")
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Booking.objects.count(), 3)
    
    def test_create_booking_missing_fields(self):
        url = reverse(
            "book_online",
            kwargs={"hotel_id": self.hotel.id, "room_id": self.room.id},
        )     
        payload = {"guest_name": "Only Name"}  
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.guest_token}")
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Booking.objects.count(), 3)

    def test_create_booking_room_not_found(self):
        bad_url = reverse(
            "book_online",
            kwargs={"hotel_id": self.hotel.id, "room_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"},
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.guest_token}")
        response = self.client.post(bad_url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_booking_unauthenticated(self):
        url = reverse(
            "book_online",
            kwargs={"hotel_id": self.hotel.id, "room_id": self.room.id},
        )     
        response = self.client.post(url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_booking_tied_to_authenticated_user(self):
        url = reverse(
            "book_online",
            kwargs={"hotel_id": self.hotel.id, "room_id": self.room.id},
        )     
        payload = self.valid_payload.copy()
        payload["user"] = str(self.admin_user.id)  # try to override

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.guest_token}")
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        booking = Booking.objects.filter(start_date=str(date.today()))
        self.assertEqual(booking[0].user, self.test_user) 

    ###Update booking
    def test_successful_booking_update(self):
        url = reverse(
            "update_user_booking",
            kwargs={"id": self.test_user.id, "booking_id": self.booking.id}
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.guest_token}")
        response = self.client.patch(url, self.update_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_booking = Booking.objects.get(id=self.booking.id)
        self.assertEqual(updated_booking.number_of_adults, 3)
        self.assertEqual(updated_booking.number_of_children, 0)
        self.assertEqual(updated_booking.guest_name, "John Updated")
        self.assertEqual(updated_booking.guest_phone, "+251911111111")

    def test_update_booking_permission_denied(self):
        url = reverse(
            "update_user_booking",
            kwargs={"id": self.test_user.id, "booking_id": self.booking.id}
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        response = self.client.put(url, self.update_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_booking_not_found(self):
        fake_booking_id = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
        url = reverse(
            "update_user_booking",
            kwargs={"id": self.test_user.id, "booking_id": fake_booking_id}
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.guest_token}")
        response = self.client.put(url, self.update_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    ###List
    def test_list_user_bookings(self):
        url = reverse("user_booking_list", kwargs={"id": self.test_user.id})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.guest_token}")
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        booking_ids = [booking['id'] for booking in response.data['results']]
        self.assertIn(str(self.booking1.id), booking_ids)
        self.assertIn(str(self.booking.id), booking_ids)
        # Ensure other user's booking is not in the list
        self.assertNotIn(str(self.other_booking.id), booking_ids)

    def test_retrieve_user_booking(self):
        url = reverse("user_booking_detail", kwargs={"id": self.test_user.id, "booking_id": self.booking1.id})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.guest_token}")
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(self.booking1.id))
        self.assertEqual(response.data["guest_name"], "John Doe")

    def test_retrieve_other_user_booking_forbidden(self):
        url = reverse("user_booking_detail", kwargs={"id": self.test_user.id, "booking_id": self.other_booking.id})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.guest_token}")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    ###cancel
    def test_cancel_own_booking(self):
        url = reverse(
            "cancel_user_booking",
            kwargs={"id": self.test_user.id, "booking_id": self.booking1.id}
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.guest_token}")
        response = self.client.patch(url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.booking1.refresh_from_db()
        self.assertEqual(self.booking1.status, "Cancelled")

    def test_cancel_other_user_booking_forbidden(self):
        url = reverse(
            "cancel_user_booking",
            kwargs={"id": self.test_user.id, "booking_id": self.other_booking.id}
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.guest_token}")
        response = self.client.patch(url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.other_booking.refresh_from_db()
        self.assertNotEqual(self.other_booking.status, "Cancelled")

    ##User history
    def test_user_can_list_own_history(self):
        url = reverse("list_user_booking_history", kwargs={"id": self.test_user.id})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.guest_token}")
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_user_cannot_list_others_history(self):
        url = reverse("list_user_booking_history", kwargs={"id": self.test_user.id})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.test_user_token}")
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_list_any_users_history(self):
        url = reverse("list_user_booking_history", kwargs={"id": self.test_user.id})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
    
    def test_user_can_retrieve_own_history(self):
        url = reverse(
            "retrieve_user_booking_history",
            kwargs={"id": self.test_user.id, "history_id": self.user_history1.id}
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.guest_token}")
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(self.user_history1.id))
        self.assertEqual(response.data["user"], self.test_user.id)

    def test_user_cannot_retrieve_others_history(self):
        url = reverse(
            "retrieve_user_booking_history",
            kwargs={"id": self.test_user1.id, "history_id": self.other_user_history.id}
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.guest_token}")
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_retrieve_any_users_history(self):
        url = reverse(
            "retrieve_user_booking_history",
            kwargs={"id": self.test_user.id, "history_id": self.user_history1.id}
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(self.user_history1.id))

    ###Delete user history
    def test_user_can_delete_own_history(self):
        url = reverse("delete_user_booking_history", kwargs={"id": self.test_user.id, "history_id": self.user_history1.id})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.guest_token}")
        response = self.client.delete(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(UserHistory.objects.filter(id=self.user_history1.id).exists())

    def test_user_cannot_delete_others_history(self):
        url = reverse("delete_user_booking_history", kwargs={"id": self.test_user.id, "history_id": self.user_history1.id})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        response = self.client.delete(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(UserHistory.objects.filter(id=self.user_history1.id).exists())

    ##Favorite
    def test_user_can_create_favorite(self):
        url = reverse("create_favorite", kwargs={"hotel_id": self.hotel.id})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.guest_token}")
        response = self.client.post(url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Favorite.objects.filter(user=self.test_user, hotel=self.hotel.id).exists())

    def test_user_can_list_their_favorites(self):
        url = reverse("list_guest_favorites", kwargs={"id": self.test_user.id})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.guest_token}")
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_user_can_retrieve_own_favorite(self):
        url = reverse("retrieve_guest_favorite", kwargs={
            "id": self.test_user.id,
            "favorite_id": self.favorite.id
        })
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.guest_token}")
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(self.favorite.id))
    
    def test_user_cannot_retrieve_others_favorite(self):
        url = reverse("retrieve_guest_favorite", kwargs={
            "id": self.test_user.id,
            "favorite_id": self.favorite.id
        })
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.test_user_token}")
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_delete_own_favorite(self):
        url = reverse("delete_guest_favorite", kwargs={
            "id": self.test_user.id,
            "favorite_id": self.favorite.id
        })
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.guest_token}")
        response = self.client.delete(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Favorite.objects.filter(id=self.favorite.id).exists())

    def test_user_cannot_delete_others_favorite(self):
        url = reverse("delete_guest_favorite", kwargs={
            "id": self.test_user.id,
            "favorite_id": self.favorite.id
        })
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        response = self.client.delete(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Favorite.objects.filter(id=self.favorite.id).exists())
     
    def test_admin_can_retrieve_any_favorite(self):
        url = reverse("retrieve_guest_favorite", kwargs={
            "id": self.test_user.id,
            "favorite_id": self.favorite.id
        })
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(self.favorite.id))