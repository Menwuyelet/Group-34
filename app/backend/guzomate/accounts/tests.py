# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken

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
        self.assertEqual(User.objects.filter(role='Guest').count(), 1)


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
            "email": "test@gmail.com",
            "password": "normaluser"
        }
        response = self.client.post(url_auth, guest_creds, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        guest_token = response.data['access']
        guest_id = response.data['id']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {guest_token}')

        url_detail = reverse('retrieve_user', kwargs={"id": guest_id})
        response = self.client.get(url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], guest_creds["email"])
        
        ## update user with self
        update_data = {
            "email": "test1@gmail.com",
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
            "email": "test@gmail.com",
            "password": "normaluser"
        }
        response = self.client.post(url_auth, guest_creds, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        guest_id = response.data['id']
    
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
            "email": "test1@gmail.com",
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
        admin_id= response.data.get('id')
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


    def test_owner_creation(self):
        url_auth = reverse('token_obtain_pair')
        admin_creds = {
            "email": "admin@example.com",
            "password": "adminpass"
        }
        response = self.client.post(url_auth, admin_creds, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        admin_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')
        
        ## valid data
        admin_url = reverse('create_owner')
        owner_data = {
            "email": "owner@example.com",
            "first_name": "owner",
            "last_name": "User",
            "phone": "0930000000",
            "gender": "Male",
            "nationality": "Ethiopian",
            "password": "admintestpas@1"
        }

        response = self.client.post(admin_url, owner_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], owner_data['email'])
        self.assertEqual(response.data['role'], "Owner")

        ## invalid data
        admin_url = reverse('create_owner')
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

        ## owners retrieve
        owner_url = reverse('list_owners')
        ## valid user
        response = self.client.get(owner_url)
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
        response = self.client.get(owner_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

