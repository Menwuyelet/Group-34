from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import City, Location, LocalAttraction, HotelCities
from hotel.models import Hotel
from accounts.models import User  # adjust import
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class BusinessViewsTest(APITestCase):
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

        self.location = Location.objects.create(
            latitude=9.0, longitude=38.7, local_name="Addis Ababa"
        )

        self.hotel = Hotel.objects.create(
            owner=self.owner_user.id,
            name="Test Hotel",
            star=4,
            location=self.location
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

        # Tokens
        self.admin_tokens = get_tokens_for_user(self.admin_user)
        self.owner_tokens = get_tokens_for_user(self.owner_user)
        self.user_tokens = get_tokens_for_user(self.normal_user)
        self.manager_tokens = get_tokens_for_user(self.manager_user)
        self.receptionist_tokens = get_tokens_for_user(self.receptionist_user)

        self.valid_city = {
            "name": "Adama",
            "description": "Capital city of Ethiopia",
            "location": {
                "latitude": 90,
                "longitude": 38.74,
                "local_name": "Central Ethiopia"
            }
        }

        self.location = Location.objects.create(latitude=9.03, longitude=38.74)
        self.city = City.objects.create(
            name="Addis Ababa",
            description="Capital city",
            location=self.location
        )

        
        self.valid_update = {
            "name": "Updated City",
            "description": "Updated description",
            "location": {
                "latitude": 10.0,
                "longitude": 40.0,
                "local_name": "updated name"
            }
        }
        # self.location1 = location={"latitude": 9.03, "longitude": 38.74, "local_name": "test1"}
        # self.location2 = location={"latitude": 10, "longitude": 11, "local_name": "test1"}
        self.city1 = City.objects.create(
            name="Addis Ababa",
            description="Capital city of Ethiopia",

        )
        self.city2 = City.objects.create(
            name="Gondar",
            description="Historical city",
        )

        self.attraction = LocalAttraction.objects.create(
            name="National Museum",
            description="Home of Lucy fossil",
            location = self.location,
            city=self.city1
        )

    def test_admin_can_create_city_successfully(self):
        url = reverse('create_city')
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_tokens['access']}")
        response = self.client.post(url, self.valid_city, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(City.objects.count(), 4)
        self.assertEqual(Location.objects.count(), 3)

    def test_non_admin_cannot_create_city(self):
        url = reverse('create_city')
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_tokens['access']}")
        response = self.client.post(url, self.valid_city, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(City.objects.count(), 3)

    def test_unauthenticated_user_cannot_create_city(self):
        url = reverse('create_city')
        response = self.client.post(url, self.valid_city, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(City.objects.count(), 3)


    def test_missing_required_field_name(self):
        invalid_city = {
            "description": "City with no name",
            "location": {
                "latitude": 10.0,
                "longitude": 40.0
            }
        }
        url = reverse('create_city')
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_tokens['access']}")
        response = self.client.post(url, invalid_city, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Location.objects.count(), 2)
        self.assertEqual(City.objects.count(), 3)

    def test_invalid_location_data(self):
        invalid_city = {
            "name": "Bad City",
            "description": "Invalid location format",
            "location": {
                "latitude": "invalid_lat",
                "longitude": 40.0
            }
        }
        url = reverse('create_city')
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_tokens['access']}")
        response = self.client.post(url, invalid_city, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Location.objects.count(), 2)
        self.assertEqual(City.objects.count(), 3)

    def test_partial_location_fields(self):
        invalid_city = {
            "name": "Half City",
            "description": "Missing longitude",
            "location": {
                "latitude": 10.0
            }
        }
        url = reverse('create_city')
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_tokens['access']}")
        response = self.client.post(url, invalid_city, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("longitude", str(response.data).lower())
        self.assertEqual(City.objects.count(), 3)

    def test_admin_can_update_city_successfully(self):
        url = reverse('update_city', kwargs={'city_id': self.city.id})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_tokens['access']}")
        response = self.client.put(url, self.valid_update, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.city.refresh_from_db()
        self.assertEqual(self.city.name, "Updated City")
        self.assertEqual(self.city.description, "Updated description")
        self.assertEqual(self.city.location.latitude, 10.0)
        self.assertEqual(self.city.location.longitude, 40.0)

    def test_non_admin_cannot_update_city(self):
        url = reverse("update_city", kwargs={"city_id": self.city.id})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_tokens['access']}")
        response = self.client.put(url, self.valid_update, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.city.refresh_from_db()
        self.assertEqual(self.city.name, "Addis Ababa")


    def test_unauthenticated_user_cannot_update_city(self):
        url = reverse("update_city", kwargs={"city_id": self.city.id})
        response = self.client.put(url, self.valid_update, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.city.refresh_from_db()
        self.assertEqual(self.city.name, "Addis Ababa") 

    def test_admin_can_delete_city(self):
        url = reverse("delete_city", kwargs={"city_id": self.city.id})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_tokens['access']}")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(City.objects.filter(id=self.city.id).exists())

        ## deleting city that doesn't exist
        url = reverse("delete_city", kwargs={"city_id": self.city.id})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_tokens['access']}")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cannot_delete_city(self):
        url = reverse("delete_city", kwargs={"city_id": self.city.id})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_tokens['access']}")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(City.objects.filter(id=self.city.id).exists())

    def test_unauthenticated_cannot_delete_city(self):
        url = reverse("delete_city", kwargs={"city_id": self.city.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(City.objects.filter(id=self.city.id).exists())

    def test_list_cities_success(self):
        url = reverse("list_cities")  # because it's a ViewSet
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data['results'][0]["name"], "Addis Ababa")
        self.assertEqual(response.data['results'][2]["name"], "Gondar")

    def test_retrieve_city_success(self):
        url = reverse("retrieve_city", kwargs={"city_id": self.city1.id})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Addis Ababa")
        self.assertEqual(response.data["description"], "Capital city of Ethiopia")

    def test_create_local_attraction(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_tokens['access']}")
        url = reverse("create_city_attraction", kwargs={"city_id": self.city1.id})
        local_attraction_data = {
            "name": "Eiffel Tower",
            "description": "Famous landmark in Paris",
            "accessibility": "Free",
            "type": "Historical",
            "location": {
                "latitude": 48.8584,
                "longitude": 2.2945,
                "local_name": "AA"
            },
            "availability": "True"
        }
        response = self.client.post(url, local_attraction_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LocalAttraction.objects.count(), 2)

    def test_update_local_attraction(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_tokens['access']}")
        url = reverse(
            "update_city_attraction",
            args=[self.city1.id, self.attraction.id]
        )
        update_data = {
            "name": "Louvre Updated",
            "description": "Updated description",
            "accessibility": "Paid",
            "type": "Museum",
            "location": {
                "latitude": 48.8606,
                "longitude": 2.3376,
                "local_name": "AA"
            },
            "availability": False
        }
        response = self.client.put(url, update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Louvre Updated")
        self.assertEqual(response.data["availability"], False)

    def test_delete_local_attraction(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_tokens['access']}")
        url = reverse(
            "delete_city_attraction",
            args=[self.city1.id, self.attraction.id]
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(LocalAttraction.objects.filter(id=self.attraction.id).exists())

    def test_list_city_local_attractions(self):
        url = reverse("list_city_attractions", args=[self.city1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertIn("name", response.data['results'][0])


    # def test_admin_can_create_hotel_city(self):
    #     url = reverse('hotelcity-create', kwargs={'hotel_id': self.hotel.id})
    #     self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_tokens['access']}")
    #     response = self.client.post(url, self.valid_hotel_city, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(HotelCities.objects.count(), 1)
    #     self.assertEqual(HotelCities.objects.first().hotel, self.hotel)
    #     self.assertEqual(HotelCities.objects.first().city, self.city)