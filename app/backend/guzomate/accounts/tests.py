# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User
from .serializers import GuestSerializer
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
        url = reverse('user_create')
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
        url = reverse('user_create')
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
        url_listing = reverse('user_list')
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

        url_detail = reverse('user_detail', kwargs={"id": guest_id})
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
        url_detail = reverse('user_detail', kwargs={"id": guest_id})
        response = self.client.get(url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], guest_creds["email"])
        url_detail = reverse('user_detail', kwargs={'id': guest_id})
        
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
        url_detail = reverse('user_detail', kwargs={'id': admin_id})

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

        url_update = reverse('user_detail', kwargs={"id": admin_id})
        update_data = {
            "email": "admin1@gmail.com"
        }

        response = self.client.patch(url_update, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # self.assertEqual(response.data["email"], data["email"])
    #     response = self.client.post(url_auth, data, format='json')
    #     token = response.data.get('access')
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    #     user = self.client.get(url_detail)
    #     self.assertEqual(user.email, data['email'])
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
       
    #     # Manager can create
    #     tokens = get_tokens_for_user(self.manager_user)
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
    #     response = self.client.post(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(response.data['email'], data['email'])

    # def test_create_user_as_admin(self):
    #     url = reverse('user_create')
    #     data = {
    #         "email": "newuser@example.com",
    #         "first_name": "New",
    #         "last_name": "User",
    #         "role": "staff",
    #         "password": "newuserpass"
    #     }

    #     # Admin can create
    #     tokens = get_tokens_for_user(self.admin_user)
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
    #     response = self.client.post(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(response.data['email'], data['email'])

    # def test_retrieve_update_delete_user_as_unauthenticated_user(self):
    #     # Create a user to retrieve/update/delete
    #     user = User.objects.create_user(
    #         email="target@example.com",
    #         first_name="Target",
    #         last_name="User",
    #         role="staff",
    #         password="targetpass"
    #     )
    #     url = reverse('user_detail', kwargs={'pk': user.id})

    #     # Unauthorized user (no auth)
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    # def test_retrieve_update_delete_user_as_staff_user(self):
    #     # Create a user to retrieve/update/delete
    #     user = User.objects.create_user(
    #         email="target@example.com",
    #         first_name="Target",
    #         last_name="User",
    #         role="staff",
    #         password="targetpass"
    #     )
    #     url = reverse('user_detail', kwargs={'pk': user.id})

    #     # staff user
    #     tokens = get_tokens_for_user(self.staff_user)
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #     self.assertEqual(response.data['detail'], "You do not have permission to view this profile.")


    # def test_retrieve_update_delete_user_as_authorized_user(self):
    #     # Create a user to retrieve/update/delete
    #     user = User.objects.create_user(
    #         email="target@example.com",
    #         first_name="Target",
    #         last_name="User",
    #         role="staff",
    #         password="targetpass"
    #     )
    #     url = reverse('user_detail', kwargs={'pk': user.id})

    #     tokens = get_tokens_for_user(user)
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['email'], "target@example.com")

    #     # Owner update
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')  # manager token
    #     update_data = {"first_name": "UpdatedName"}
    #     response = self.client.patch(url, update_data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['first_name'], "UpdatedName")

    #     # Owner delete - test owner deleting own user
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertFalse(User.objects.filter(id=user.id).exists())

    # def test_retrieve_update_delete_user_as_manager(self):
    #     # Create a user to retrieve/update/delete
    #     user = User.objects.create_user(
    #         email="target@example.com",
    #         first_name="Target",
    #         last_name="User",
    #         role="staff",
    #         password="targetpass"
    #     )
    #     url = reverse('user_detail', kwargs={'pk': user.id})
    #     # Manager can retrieve
    #     tokens = get_tokens_for_user(self.manager_user)
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
 

    # def test_list_users_as_unauthorized_user(self):
    #     url = reverse('user_list')

    #     # Unauthenticated user
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    # def test_list_users_as_staff(self):
    #     url = reverse('user_list')

    #     # Staff user forbidden
    #     tokens = get_tokens_for_user(self.staff_user)
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # def test_list_users_as_manager(self):
    #     url = reverse('user_list')
    #     # Manager can list
    #     tokens = get_tokens_for_user(self.manager_user)
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     # Should include all users
    #     emails = [u['email'] for u in response.data['results']]
    #     self.assertIn(self.admin_user.email, emails)
    #     self.assertIn(self.staff_user.email, emails)
    #     self.assertIn(self.manager_user.email, emails)

    # def test_serializer_validation(self):

    #     # Missing email
    #     serializer = UserSerializer(data={
    #         "first_name": "Test",
    #         "last_name": "User",
    #         "password": "pass"
    #     })
    #     self.assertFalse(serializer.is_valid())
    #     self.assertIn('email', serializer.errors)

    #     # Missing first_name
    #     serializer = UserSerializer(data={
    #         "email": "test@example.com",
    #         "last_name": "User",
    #         "password": "pass"
    #     })
    #     self.assertFalse(serializer.is_valid())
    #     self.assertIn('first_name', serializer.errors)

    #     # Missing last_name
    #     serializer = UserSerializer(data={
    #         "email": "test@example.com",
    #         "first_name": "Test",
    #         "password": "pass"
    #     })
    #     self.assertFalse(serializer.is_valid())
    #     self.assertIn('last_name', serializer.errors)

    #     # Missing role
    #     serializer = UserSerializer(data={
    #         "email": "valid@example.com",
    #         "first_name": "Valid",
    #         "last_name": "User",
    #         "password": "pass"
    #     })
    #     self.assertFalse(serializer.is_valid())
    #     self.assertIn('role', serializer.errors)

    #     # Missing role
    #     serializer = UserSerializer(data={
    #         "email": "valid@example.com",
    #         "first_name": "Valid",
    #         "last_name": "User",
    #         "password": "pass",
    #         "role": "manager"
    #     })
    #     self.assertTrue(serializer.is_valid())