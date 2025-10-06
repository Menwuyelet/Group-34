# GuzoMate API Documentation

This document provides the API design for the GuzoMate project, structured into three main user roles: Guests, Hotel Management, and Administrators.

---

## Authentication

| Method | Path | Description | Permissions |
|--------|------|-------------|-------------|
| POST | `/api/auth/login/` | User login with email/password | Public |
| POST | `/api/auth/refresh/` | Refresh access token | Public |

---

## Admin Endpoints

### Admin Management
| Method | Path | Description | Permissions |
|--------|------|-------------|-------------|
| GET | `/api/admin/admins/` | List all admin users | Admin only |
| POST | `/api/admin/admins/` | Create new admin user | Admin only |
| GET | `/api/admin/admins/{id}/` | Get admin user details | Admin only |
| PUT | `/api/admin/admins/{id}/` | Update admin user | Admin only |
| PATCH | `/api/admin/admins/{id}/` | Partial update admin user | Admin only |
| DELETE | `/api/admin/admins/{id}/` | Delete admin user | Admin only |

### Owner Management
| Method | Path | Description | Permissions |
|--------|------|-------------|-------------|
| GET | `/api/admin/owners/list/` | List all owners | Admin only |
| POST | `/api/admin/owners/create/` | Create new owner | Admin only |
| GET | `/api/admin/owners/{id}/` | Get owner details | Admin only |
| PUT | `/api/admin/owners/{id}/` | Update owner | Admin only |
| PATCH | `/api/admin/owners/{id}/` | Partial update owner | Admin only |
| DELETE | `/api/admin/owners/{id}/` | Delete owner | Admin only |

### Guest Management
| Method | Path | Description | Permissions |
|--------|------|-------------|-------------|
| GET | `/api/admin/guest/list/` | List all guests | Admin only |
| GET | `/api/admin/guest/{id}/` | Get guest details | Admin only |
| PUT | `/api/admin/guest/{id}/` | Update guest | Admin only |
| PATCH | `/api/admin/guest/{id}/` | Partial update guest | Admin only |
| DELETE | `/api/admin/guest/{id}/` | Delete guest | Admin only |

### City Management
| Method | Path | Description | Permissions |
|--------|------|-------------|-------------|
| POST | `/api/admin/cities/create/` | Create new city | Admin only |
| PUT | `/api/admin/city/{city_id}/update/` | Update city | Admin only |
| PATCH | `/api/admin/city/{city_id}/update/` | Partial update city | Admin only |
| DELETE | `/api/admin/city/{city_id}/delete/` | Delete city | Admin only |

### City Images Management
| Method | Path | Description | Permissions |
|--------|------|-------------|-------------|
| PUT | `/api/admin/city/{city_id}/image/create/` | Upload city image | Admin only |
| PATCH | `/api/admin/city/{city_id}/image/create/` | Update city image | Admin only |
| PUT | `/api/admin/city/{city_id}/image/{image_id}/update/` | Update specific city image | Admin only |
| PATCH | `/api/admin/city/{city_id}/image/{image_id}/update/` | Partial update city image | Admin only |
| DELETE | `/api/admin/city/{city_id}/image/{image_id}/delete/` | Delete city image | Admin only |

### Local Attractions Management
| Method | Path | Description | Permissions |
|--------|------|-------------|-------------|
| POST | `/api/admin/city/{city_id}/attraction/create/` | Create local attraction | Admin only |
| PUT | `/api/admin/city/{city_id}/attraction/{attraction_id}/update/` | Update attraction | Admin only |
| PATCH | `/api/admin/city/{city_id}/attraction/{attraction_id}/update/` | Partial update attraction | Admin only |
| DELETE | `/api/admin/city/{city_id}/attraction/{attraction_id}/delete/` | Delete attraction | Admin only |

---

## Guest Endpoints

### Guest Profile
| Method | Path | Description | Permissions |
|--------|------|-------------|-------------|
| POST | `/api/guest/create/` | Register as guest | Public |
| GET | `/api/guest/{id}/` | Get guest profile | Authenticated user |
| PUT | `/api/guest/{id}/` | Update guest profile | Authenticated user |
| PATCH | `/api/guest/{id}/` | Partial update profile | Authenticated user |
| DELETE | `/api/guest/{id}/` | Delete guest account | Authenticated user |

### Guest Bookings
| Method | Path | Description | Permissions |
|--------|------|-------------|-------------|
| GET | `/api/guest/{id}/bookings` | List guest bookings | Authenticated user |
| GET | `/api/guest/{id}/booking/{booking_id}` | Get booking details | Authenticated user |
| PUT | `/api/guest/{id}/booking/{booking_id}/update/` | Update booking | Authenticated user |
| PATCH | `/api/guest/{id}/booking/{booking_id}/update/` | Partial update booking | Authenticated user |
| PUT | `/api/guest/{id}/booking/{booking_id}/cancel/` | Cancel booking | Authenticated user |
| PATCH | `/api/guest/{id}/booking/{booking_id}/cancel/` | Partial cancel booking | Authenticated user |

### Guest Favorites
| Method | Path | Description | Permissions |
|--------|------|-------------|-------------|
| GET | `/api/guest/{id}/favorites/` | List favorite hotels | Authenticated user |
| GET | `/api/guest/{id}/favorite/{favorite_id}` | Get favorite details | Authenticated user |
| DELETE | `/api/guest/{id}/favorite/{favorite_id}/delete/` | Remove from favorites | Authenticated user |

### Guest History
| Method | Path | Description | Permissions |
|--------|------|-------------|-------------|
| GET | `/api/guest/{id}/history` | List booking history | Authenticated user |
| GET | `/api/guest/{id}/history/{history_id}` | Get history details | Authenticated user |
| DELETE | `/api/guest/{id}/history/{history_id}/delete` | Delete history record | Authenticated user |

### Guest Reviews
| Method | Path | Description | Permissions |
|--------|------|-------------|-------------|
| GET | `/api/guest/{id}/reviews/` | List guest reviews | Authenticated user |
| GET | `/api/guest/{id}/review/{review_id}/detail/` | Get review details | Authenticated user |
| PUT | `/api/guest/{id}/review/{review_id}/update/` | Update review | Authenticated user |
| PATCH | `/api/guest/{id}/review/{review_id}/update/` | Partial update review | Authenticated user |
| DELETE | `/api/guest/{id}/review/{review_id}/delete/` | Delete review | Authenticated user |

### Guest Cities & Attractions
| Method | Path | Description | Permissions |
|--------|------|-------------|-------------|
| GET | `/api/guest/cities/` | List all cities | Public |
| GET | `/api/guest/city/{city_id}/` | Get city details | Public |
| GET | `/api/guest/city/{city_id}/images/list/` | List city images | Public |
| GET | `/api/guest/city/{city_id}/image/{image_id}/retrieve/` | Get city image | Public |
| GET | `/api/guest/city/{city_id}/attractions/list/` | List city attractions | Public |
| GET | `/api/guest/city/{city_id}/attraction/detail/` | Get attraction details | Public |

---

## Hotel Management Endpoints

### Hotel Operations
| Method | Path | Description | Permissions |
|--------|------|-------------|-------------|
| POST | `/api/hotel/create/` | Create new hotel | Owner/Admin |
| GET | `/api/hotel/list/` | List all hotels | Public |
| GET | `/api/hotel/{hotel_id}/retrieve/` | Get hotel details | Public |
| PUT | `/api/hotel/{hotel_id}/update/` | Update hotel | Manager/Owner/Admin |
| PATCH | `/api/hotel/{hotel_id}/update/` | Partial update hotel | Manager/Owner/Admin |
| DELETE | `/api/hotel/{hotel_id}/delete/` | Delete hotel | Owner/Admin |

### Hotel Staff Management
| Method | Path | Description | Permissions |
|--------|------|-------------|-------------|
| POST | `/api/hotel/{hotel_id}/staff/` | Add staff member | Manager/Owner/Admin |
| GET | `/api/hotel/{hotel_id}/staff/list/` | List hotel staff | Manager/Owner/Admin |
| GET | `/api/hotel/{hotel_id}/staff/{staff_id}` | Get staff details | Manager/Owner/Admin |
| PUT | `/api/hotel/{hotel_id}/staff/{staff_id}` | Update staff | Manager/Owner/Admin |
| PATCH | `/api/hotel/{hotel_id}/staff/{staff_id}` | Partial update staff | Manager/Owner/Admin |
| DELETE | `/api/hotel/{hotel_id}/staff/{staff_id}` | Remove staff | Manager/Owner/Admin |

### Room Management
| Method | Path | Description | Permissions |
|--------|------|-------------|-------------|
| POST | `/api/hotel/{hotel_id}/create-room/` | Create room | Manager/Owner/Admin |
| GET | `/api/hotel/{hotel_id}/rooms/` | List hotel rooms | Public |
| GET | `/api/hotel/{hotel_id}/retrieve-room/{room_id}` | Get room details | Public |
| PUT | `/api/hotel/{hotel_id}/update-room/{room_id}` | Update room | Manager/Owner/Admin |
| PATCH | `/api/hotel/{hotel_id}/update-room/{room_id}` | Partial update room | Manager/Owner/Admin |
| DELETE | `/api/hotel/{hotel_id}/delete-room/{room_id}` | Delete room | Manager/Owner/Admin |

### Room Amenities
| Method | Path | Description | Permissions |
|--------|------|-------------|-------------|
| POST | `/api/hotel/{hotel_id}/room/{room_id}/amenity/create/` | Add room amenity | Manager/Owner/Admin |
| GET | `/api/hotel/{hotel_id}/room/{room_id}/amenities/` | List room amenities | Public |
| GET | `/api/hotel/{hotel_id}/room/{room_id}/amenity/{amenity_id}/` | Get amenity details | Public |
| PUT | `/api/hotel/{hotel_id}/room/{room_id}/amenity/{amenity_id}/update/` | Update amenity | Manager/Owner/Admin |
| PATCH | `/api/hotel/{hotel_id}/room/{room_id}/amenity/{amenity_id}/update/` | Partial update amenity | Manager/Owner/Admin |
| DELETE | `/api/hotel/{hotel_id}/room/{room_id}/amenity/{amenity_id}/delete/` | Delete amenity | Manager/Owner/Admin |

### Hotel Amenities
| Method | Path | Description | Permissions |
|--------|------|-------------|-------------|
| POST | `/api/hotel/{hotel_id}/amenity/create/` | Add hotel amenity | Manager/Owner/Admin |
| GET | `/api/hotel/{hotel_id}/amenities/` | List hotel amenities | Public |
| GET | `/api/hotel/{hotel_id}/amenity/{amenity_id}/` | Get amenity details | Public |
| PUT | `/api/hotel/{hotel_id}/amenity/{amenity_id}/update/` | Update amenity | Manager/Owner/Admin |
| PATCH | `/api/hotel/{hotel_id}/amenity/{amenity_id}/update/` | Partial update amenity | Manager/Owner/Admin |
| DELETE | `/api/hotel/{hotel_id}/amenity/{amenity_id}/delete/` | Delete amenity | Manager/Owner/Admin |

### Hotel Images
| Method | Path | Description | Permissions |
|--------|------|-------------|-------------|
| POST | `/api/hotel/{hotel_id}/image/create-image/` | Upload hotel image | Manager/Owner/Admin |
| GET | `/api/hotel/{hotel_id}/images/` | List hotel images | Public |
| GET | `/api/hotel/{hotel_id}/image/{image_id}` | Get image details | Public |
| PUT | `/api/hotel/{hotel_id}/image/{image_id}/update-image/` | Update image | Manager/Owner/Admin |
| PATCH | `/api/hotel/{hotel_id}/image/{image_id}/update-image/` | Partial update image | Manager/Owner/Admin |
| DELETE | `/api/hotel/{hotel_id}/image/{image_id}/delete-image/` | Delete image | Manager/Owner/Admin |

### Room Images
| Method | Path | Description | Permissions |
|--------|------|-------------|-------------|
| POST | `/api/hotel/{hotel_id}/room/{room_id}/image/create/` | Upload room image | Manager/Owner/Admin |
| GET | `/api/hotel/{hotel_id}/room/{room_id}/images/` | List room images | Public |
| GET | `/api/hotel/{hotel_id}/room/{room_id}/image/{image_id}/` | Get room image | Public |
| PUT | `/api/hotel/{hotel_id}/room/{room_id}/image/{image_id}/update/` | Update room image | Manager/Owner/Admin |
| PATCH | `/api/hotel/{hotel_id}/room/{room_id}/image/{image_id}/update/` | Partial update room image | Manager/Owner/Admin |
| DELETE | `/api/hotel/{hotel_id}/room/{room_id}/image/{image_id}/delete/` | Delete room image | Manager/Owner/Admin |

### Hotel Events
| Method | Path | Description | Permissions |
|--------|------|-------------|-------------|
| POST | `/api/hotel/{hotel_id}/event/create/` | Create event | Manager/Owner/Admin |
| GET | `/api/hotel/{hotel_id}/events/` | List hotel events | Public |
| GET | `/api/hotel/{hotel_id}/event/{event_id}/` | Get event details | Public |
| PUT | `/api/hotel/{hotel_id}/event/{event_id}/update/` | Update event | Manager/Owner/Admin |
| PATCH | `/api/hotel/{hotel_id}/event/{event_id}/update/` | Partial update event | Manager/Owner/Admin |
| DELETE | `/api/hotel/{hotel_id}/event/{event_id}/delete/` | Delete event | Manager/Owner/Admin |

### Event Images
| Method | Path | Description | Permissions |
|--------|------|-------------|-------------|
| POST | `/api/hotel/{hotel_id}/event/{event_id}/image/create/` | Upload event image | Manager/Owner/Admin |
| GET | `/api/hotel/{hotel_id}/event/{event_id}/images/` | List event images | Public |
| GET | `/api/hotel/{hotel_id}/event/{event_id}/image/{image_id}/` | Get event image | Public |
| PUT | `/api/hotel/{hotel_id}/event/{event_id}/image/{image_id}/update/` | Update event image | Manager/Owner/Admin |
| PATCH | `/api/hotel/{hotel_id}/event/{event_id}/image/{image_id}/update/` | Partial update event image | Manager/Owner/Admin |
| DELETE | `/api/hotel/{hotel_id}/event/{event_id}/image/{image_id}/delete/` | Delete event image | Manager/Owner/Admin |

### Hotel Cities
| Method | Path | Description | Permissions |
|--------|------|-------------|-------------|
| POST | `/api/hotel/{hotel_id}/city/create/` | Add hotel city | Manager/Owner/Admin |
| GET | `/api/hotel/{hotel_id}/cities/` | List hotel cities | Public |
| PUT | `/api/hotel/{hotel_id}/city/{hotel_city_id}/update/` | Update hotel city | Manager/Owner/Admin |
| PATCH | `/api/hotel/{hotel_id}/city/{hotel_city_id}/update/` | Partial update hotel city | Manager/Owner/Admin |
| DELETE | `/api/hotel/{hotel_id}/city/{hotel_city_id}/delete/` | Remove hotel city | Manager/Owner/Admin |

### Local Attractions (Hotel)
| Method | Path | Description | Permissions |
|--------|------|-------------|-------------|
| POST | `/api/hotel/{hotel_id}/attraction/create` | Add hotel attraction | Manager/Owner/Admin |
| GET | `/api/hotel/{hotel_id}/attractions/list` | List hotel attractions | Public |
| GET | `/api/hotel/{hotel_id}/attraction/{attraction_id}/retrieve` | Get attraction details | Public |
| PUT | `/api/hotel/{hotel_id}/attraction/{attraction_id}/update` | Update attraction | Manager/Owner/Admin |
| PATCH | `/api/hotel/{hotel_id}/attraction/{attraction_id}/update` | Partial update attraction | Manager/Owner/Admin |
| DELETE | `/api/hotel/{hotel_id}/attraction/{attraction_id}/delete` | Delete attraction | Manager/Owner/Admin |

### Bookings (Hotel Management)
| Method | Path | Description | Permissions |
|--------|------|-------------|-------------|
| POST | `/api/hotel/{hotel_id}/book/` | Create in-person booking | Staff/Manager/Owner/Admin |
| POST | `/api/hotel/{hotel_id}/room/{room_id}/book/` | Create room booking | Staff/Manager/Owner/Admin |
| GET | `/api/hotel/{hotel_id}/bookings` | List hotel bookings | Staff/Manager/Owner/Admin |
| GET | `/api/hotel/{hotel_id}/booking/{booking_id}/retrieve` | Get booking details | Staff/Manager/Owner/Admin |
| PUT | `/api/hotel/{hotel_id}/booking/{booking_id}/update` | Update booking | Staff/Manager/Owner/Admin |
| PATCH | `/api/hotel/{hotel_id}/booking/{booking_id}/update` | Partial update booking | Staff/Manager/Owner/Admin |
| PUT | `/api/hotel/{hotel_id}/booking/{booking_id}/status` | Update booking status | Staff/Manager/Owner/Admin |
| PATCH | `/api/hotel/{hotel_id}/booking/{booking_id}/status` | Partial update status | Staff/Manager/Owner/Admin |

### Booking History (Hotel)
| Method | Path | Description | Permissions |
|--------|------|-------------|-------------|
| GET | `/api/hotel/{hotel_id}/booking/history/local` | List local booking history | Manager/Owner/Admin |
| GET | `/api/hotel/{hotel_id}/booking/history/online` | List online booking history | Manager/Owner/Admin |
| GET | `/api/hotel/{hotel_id}/booking/history/local/{history_id}` | Get local history details | Manager/Owner/Admin |
| GET | `/api/hotel/{hotel_id}/booking/history/online/{history_id}` | Get online history details | Manager/Owner/Admin |
| DELETE | `/api/hotel/{hotel_id}/booking/history/{history_id}/delete` | Delete history record | Manager/Owner/Admin |

### Hotel Reviews
| Method | Path | Description | Permissions |
|--------|------|-------------|-------------|
| POST | `/api/hotel/{hotel_id}/review/create/` | Create review | Authenticated user |
| GET | `/api/hotel/{hotel_id}/review/list/` | List hotel reviews | Public |
| GET | `/api/hotel/{hotel_id}/review/{review_id}/detail/` | Get review details | Public |

### Favorites
| Method | Path | Description | Permissions |
|--------|------|-------------|-------------|
| POST | `/api/hotel/{hotel_id}/favorite/create/` | Add to favorites | Authenticated user |

---

## User Roles

- **Admin**: Full system access
- **Owner**: Hotel ownership and management
- **Manager**: Hotel operational management
- **Receptionist**: Booking and guest management
- **Guest**: Booking and review capabilities
- **Staff**: Limited hotel operations

---

## Booking Statuses

- **Pending**: Booking request received
- **Confirmed**: Booking confirmed
- **Checked_in**: Guest has checked in
- **Cancelled**: Booking cancelled
- **Completed**: Stay completed

## Payment Statuses

- **Pending**: Payment not yet completed
- **Completed**: Payment successful

---

## Conclusion

This API provides comprehensive hotel management capabilities with role-based access control, supporting online and in-person bookings, reviews, favorites, and extensive hotel operations management.

---

© 2025 GuzoMate Project Team