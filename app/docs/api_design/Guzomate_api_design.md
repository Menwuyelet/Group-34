# GuzoMate API Documentation

This document provides the API design for the GuzoMate project, structured into two main services:
## Booking Service (Auth: Guests, Admin)

---

### Admin Endpoints

| Method | Path                                                  | Description                          | Permissions      |
|--------|-------------------------------------------------------|------------------------------------|------------------|
| GET    | `/api/admin/users/`                                   | List all users                     | Admin only       |
| POST   | `/api/admin/users/`                                   | Create a new user                  | Admin only       |
| POST   | `/api/admin/hotels/`                                  | Create a new hotel                 | Admin only       |
| DELETE | `/api/admin/hotels/{hotel_id}/`                       | Delete a hotel                    | Admin only       |
| PUT    | `/api/admin/local-attractions/{attraction_id}/`      | Update a local attraction          | Admin only       |
| DELETE | `/api/admin/local-attractions/{attraction_id}/`      | Delete a local attraction          | Admin only       |
| POST   | `/api/admin/local-attractions/{attraction_id}/images/` | Upload an image for attraction   | Admin only       |
| DELETE | `/api/admin/local-attractions/{attraction_id}/images/{image_id}/` | Delete an image for attraction | Admin only       |
| POST   | `/api/admin/local-attractions/`                       | Create a local attraction          | Admin only       |
| POST   | `/api/admin/cities/`                                  | Create a city                     | Admin only       |
| PUT    | `/api/admin/cities/{city_id}/`                        | Update city                      | Admin only       |
| DELETE | `/api/admin/cities/{city_id}/`                        | Delete city                      | Admin only       |
| POST   | `/api/admin/cities/{city_id}/images/`                 | Upload image for city             | Admin only       |
| DELETE | `/api/admin/cities/{city_id}/images/{image_id}/`      | Delete city image                 | Admin only       |

---

### Hotel

| Method | Path                                                | Description                            | Permissions        |
|--------|-----------------------------------------------------|--------------------------------------|--------------------|
| GET    | `/api/hotels/`                                      | List all hotels                      | Public             |
| GET    | `/api/hotels/{hotel_id}/`                           | Get hotel details                   | Public             |
| GET    | `/api/hotels/{hotel_id}/pictures/`                  | List hotel pictures                 | Public             |
| GET    | `/api/hotels/{hotel_id}/pictures/{image_id}`        | Get specific hotel image details   | Public             |
| GET    | `/api/hotels/{hotel_id}/rooms/`                     | List rooms of the hotel (with availability) | Public       |
| GET    | `/api/hotels/{hotel_id}/rooms/{room_id}/`           | Get room details                   | Public             |
| GET    | `/api/hotels/{hotel_id}/local-attractions/`         | List local attractions by hotel    | Public             |
| POST   | `/api/hotels/{hotel_id}/reviews/`                   | Create a review for hotel          | Authenticated user |
| GET    | `/api/hotels/{hotel_id}/reviews/`                   | List all reviews of hotel          | Public             |

---

### Local Attractions

| Method | Path                                                 | Description                     | Permissions |
|--------|------------------------------------------------------|---------------------------------|-------------|
| GET    | `/api/local-attractions/`                            | List all local attractions      | Public      |
| GET    | `/api/local-attractions/{attraction_id}/`           | Get attraction details          | Public      |
| GET    | `/api/local-attractions/{attraction_id}/images/`    | List images for attraction      | Public      |

---

### Guest (User)

| Method | Path                                                   | Description                        | Permissions          |
|--------|--------------------------------------------------------|----------------------------------|----------------------|
| GET    | `/api/users/{user_id}/`                                | Get user details                 | Authenticated user   |
| PUT    | `/api/users/{user_id}/`                                | Update user profile             | Authenticated user   |
| GET    | `/api/users/{user_id}/reviews/`                        | List all reviews by the user    | Authenticated user   |
| PUT    | `/api/users/{user_id}/reviews/{review_id}/`            | Update a review (owner/admin)   | Authenticated user   |
| DELETE | `/api/users/{user_id}/reviews/{review_id}/`            | Delete a review (owner/admin)   | Authenticated user   |
| GET    | `/api/users/{user_id}/history/`                        | List booking history            | Authenticated user   |
| GET    | `/api/users/{user_id}/history/{history_id}/`           | Get booking history detail      | Authenticated user   |
| DELETE | `/api/users/{user_id}/history/{history_id}/`           | Delete booking history          | Authenticated user   |
| GET    | `/api/users/{user_id}/favorites/`                      | List favorites                  | Authenticated user   |
| GET    | `/api/users/{user_id}/favorites/{favorite_id}`         | Get favorite details            | Authenticated user   |
| POST   | `/api/users/{user_id}/favorites/`                      | Add a favorite                  | Authenticated user   |
| DELETE | `/api/users/{user_id}/favorites/{favorite_id}/`         | Remove a favorite               | Authenticated user   |
| DELETE | `/api/users/{user_id}/`                                | Delete user account             | Authenticated user   |

---

### Booking

| Method | Path                                              | Description                    | Permissions                 |
|--------|---------------------------------------------------|-------------------------------|-----------------------------|
| GET    | `/api/bookings/{user_id}`                         | List bookings for a user      | Authenticated user          |
| GET    | `/api/bookings/{booking_id}/`                     | Get booking details           | Authenticated user          |
| POST   | `/api/bookings/`                                  | Create a new booking          | Public (online booking)     |
| PUT    | `/api/bookings/{booking_id}/`                     | Update booking                | Authenticated user          |
| DELETE | `/api/bookings/{booking_id}/`                     | Delete booking                | Authenticated user          |

---

### City

| Method | Path                                               | Description                   | Permissions |
|--------|----------------------------------------------------|-------------------------------|-------------|
| GET    | `/api/cities/`                                     | List all cities              | Public      |
| GET    | `/api/cities/{city_id}/`                           | Get city details             | Public      |
| GET    | `/api/cities/{city_id}/images/`                    | List city images             | Public      |

---

## Management Service (Hotel Manager, Staff, Admin)

---

### Hotel

| Method | Path                                              | Description                  | Permissions            |
|--------|---------------------------------------------------|------------------------------|------------------------|
| PUT    | `/api/hotels/{hotel_id}/`                         | Update hotel info            | Manager, Admin         |

---

### Staff (Hotel)

| Method | Path                                              | Description                 | Permissions        |
|--------|---------------------------------------------------|-----------------------------|--------------------|
| GET    | `/api/hotels/{hotel_id}/staff/`                   | List hotel staff            | Manager, Admin     |
| POST   | `/api/hotels/{hotel_id}/staff/`                   | Add hotel staff             | Manager, Admin     |
| GET    | `/api/hotels/{hotel_id}/staff/{staff_id}/`        | Get staff details           | Manager, Admin     |
| PUT    | `/api/hotels/{hotel_id}/staff/{staff_id}/`        | Update staff info           | Manager, Admin     |
| DELETE | `/api/hotels/{hotel_id}/staff/{staff_id}/`        | Remove staff                | Manager, Admin     |

---

### Room (Hotel)

| Method | Path                                              | Description                | Permissions        |
|--------|---------------------------------------------------|----------------------------|--------------------|
| GET    | `/api/hotels/{hotel_id}/rooms/`                   | List rooms                 | Manager, Admin     |
| GET    | `/api/hotels/{hotel_id}/rooms/{room_id}/`         | Get room details           | Manager, Admin     |
| POST   | `/api/hotels/{hotel_id}/rooms/`                   | Create a room              | Manager, Admin     |
| PUT    | `/api/hotels/{hotel_id}/rooms/{room_id}/`         | Update room info           | Manager, Admin     |
| DELETE | `/api/hotels/{hotel_id}/rooms/{room_id}/`         | Delete a room              | Manager, Admin     |

---

### Booking (In-person and Management)

| Method | Path                                              | Description                | Permissions            |
|--------|---------------------------------------------------|----------------------------|------------------------|
| GET    | `/api/hotels/{hotel_id}/bookings/`                | List bookings              | Staff, Manager, Admin  |
| GET    | `/api/hotels/{hotel_id}/bookings/{booking_id}/`   | Booking detail             | Staff, Manager, Admin  |
| POST   | `/api/hotels/{hotel_id}/bookings/`                | Create booking (in-person) | Staff, Manager, Admin  |
| PUT    | `/api/hotels/{hotel_id}/bookings/{booking_id}/`   | Update booking             | Staff, Manager, Admin  |
| DELETE | `/api/hotels/{hotel_id}/bookings/{booking_id}/`   | Delete booking             | Staff, Manager, Admin  |

---

### Booking History (Hotel)

| Method | Path                                              | Description                | Permissions    |
|--------|---------------------------------------------------|----------------------------|----------------|
| GET    | `/api/hotels/{hotel_id}/history/`                 | List booking history       | Manager, Admin |
| GET    | `/api/hotels/{hotel_id}/history/{history_id}/`    | Booking history detail     | Manager, Admin |
| DELETE | `/api/hotels/{hotel_id}/history/{history_id}/`    | Delete booking history     | Manager, Admin |

---

### Review (Hotel)

| Method | Path                                              | Description                | Permissions    |
|--------|---------------------------------------------------|----------------------------|----------------|
| GET    | `/api/hotels/{hotel_id}/reviews/`                 | List reviews               | Public         |
| GET    | `/api/hotels/{hotel_id}/reviews/{review_id}/`     | Review detail              | Public         |

---

### Amenities (Hotel)

| Method | Path                                               | Description                | Permissions    |
|--------|----------------------------------------------------|----------------------------|----------------|
| GET    | `/api/hotels/{hotel_id}/amenities/`                | List amenities             | Manager, Admin |
| POST   | `/api/hotels/{hotel_id}/amenities/`                | Add amenity                | Manager, Admin |
| PUT    | `/api/hotels/{hotel_id}/amenities/{amenities_id}/` | Update amenity             | Manager, Admin |
| GET    | `/api/hotels/{hotel_id}/amenities/{amenities_id}/` | Amenity detail             | Manager, Admin |

---

### Events (Hotel)

| Method | Path                                               | Description                | Permissions    |
|--------|----------------------------------------------------|----------------------------|----------------|
| GET    | `/api/hotels/{hotel_id}/events/`                   | List events                | Manager, Admin |
| POST   | `/api/hotels/{hotel_id}/events/`                   | Create event               | Manager, Admin |
| PUT    | `/api/hotels/{hotel_id}/events/{event_id}/`        | Update event               | Manager, Admin |
| DELETE | `/api/hotels/{hotel_id}/events/{event_id}/`        | Delete event               | Manager, Admin |
| GET    | `/api/hotels/{hotel_id}/events/{event_id}/`        | Event detail               | Manager, Admin |

---

### Images (Hotel)

| Method | Path                                               | Description                | Permissions    |
|--------|----------------------------------------------------|----------------------------|----------------|
| GET    | `/api/hotels/{hotel_id}/images/`                    | List images                | Manager, Admin |
| POST   | `/api/hotels/{hotel_id}/images/`                    | Upload image               | Manager, Admin |
| DELETE | `/api/hotels/{hotel_id}/images/{image_id}/`         | Delete image               | Manager, Admin |

---

### Location (Hotel)

| Method | Path                                               | Description                | Permissions    |
|--------|----------------------------------------------------|----------------------------|----------------|
| GET    | `/api/hotels/{hotel_id}/locations/`                 | List locations             | Manager, Admin |
| POST   | `/api/hotels/{hotel_id}/locations/`                 | Create location            | Manager, Admin |
| PUT    | `/api/locations/{location_id}/`                      | Update location            | Manager, Admin |
| DELETE | `/api/locations/{location_id}/`                      | Delete location            | Manager, Admin |

## Conclusion

This endpoint design is structured to give a hierarchial path to access small(sub entities) via their parent entities and to ensure security by exposing certain endpoints to specific users only.

---

© 2025 GuzoMate Project Team