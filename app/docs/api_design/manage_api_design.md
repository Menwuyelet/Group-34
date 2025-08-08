# GuzoMate – API Design Documentation (Hotel management service)

This document provides the API design for the hotel management service in the GuzoMate project.

- **Hotel Management API** — manages hotels, rooms, amenities, images, and related entities.
---

### Hotels
  |Method          |Path                                       |Function
  |----------------|-------------------------------------------|---------|
  |**GET**         |`/api/hotels/`                             |List hotels  
  |**GET**         |`/api/hotels/{hotel_id}/`                  |Hotel details  
  |**POST**        |`/api/hotels/`                             |Create hotel (Site admin only)  
  |**PUT**         |`/api/hotels/{hotel_id}/`                  |Update hotel (hotel staff)  
  |**DELETE**      |`/api/hotels/{hotel_id}/`                  |Delete hotel (Site admin only)

---

### Rooms
  |Method           |Path                                       |Function
  |-----------------|-------------------------------------------|---------|
  |**GET**          |`/api/hotels/{hotel_id}/rooms/`            |List rooms for hotel  
  |**GET**          |`/api/hotels/{hotel_id}/rooms/{room_id}/`  |Room details  
  |**POST**         |`/api/hotels/{hotel_id}/rooms/`            |Create room (hotel staff) 
  |**PUT**          |`/api/hotels/{hotel_id}/rooms/{room_id}/`  |Update room (hotel staff)
  |**DELETE**       |`/api/hotels/{hotel_id}/rooms/{room_id}/`  |Delete room (hotel staff)

---

### Amenities
  |Method           |Path                                                |Function
  |-----------------|----------------------------------------------------|---------|
  |**GET**          |`/api/hotels/{hotel_id}/amenities/`                 |List amenities (hotel level)  
  |**POST**         |`/api/hotels/{hotel_id}/amenities/`                 |Create amenity (hotel staff)
  |**PUT**          |`/api/hotels/{hotel_id}/amenities/{amenities_id}/`  |Update amenity (hotel staff) 
  |**DELETE**       |`/api/hotels/{hotel_id}/{amenities_id}/`            |Delete amenity (hotel staff)
  |**GET**          |`/api/hotels/{hotel_id}/rooms/{room_id}/amenities/` |List amenities (room level)  

---

### Images
  |Method           |Path                                                                       |Function
  |-----------------|---------------------------------------------------------------------------|---------|
  |**POST**         |`/api/hotels/{hotel_id}/images/ `                                          |Upload image (hotel staff) 
  |**GET**          |`/api/hotels/{hotel_id}/images/?imageable_type={type}&imageable_id={id} `  |List images  
  |**DELETE**       |`/api/hotels/{hotel_id}/images/{image_id}/ `                               |Delete image (hotel staff)

---

### Events
  |Method           |Path                                         |Function
  |-----------------|---------------------------------------------|---------|
  |**GET**          |`/api/hotels/{hotel_id}/events/`             |List events for hotel  
  |**GET**          |`/api/hotels/{hotel_id}/events/{event_id}/`  |event details  
  |**POST**         |`/api/hotels/{hotel_id}/events/`             |Create events (hotel staff) 
  |**PUT**          |`/api/hotels/{hotel_id}/events/{event_id}/ ` |Update room (hotel staff)
  |**DELETE**       |`/api/hotels/{hotel_id}/events/{event_id}/`  |Delete room (hotel staff)

---

### Local attractions
  |Method           |Path                                                               |Function
  |-----------------|-------------------------------------------------------------------|---------|
  |**GET**          |`/api/hotels/{hotel_id}/local-attractions/    `                    |List local attraction for hotel  
  |**GET**          |`/api/hotels/{hotel_id}/local-attractions/{localAttraction_id}/`   |local-attractions details  
  |**POST**         |`/api/hotels/{hotel_id}/local-attractions/   `                     |Create local-attractions (hotel staff) 
  |**PUT**          |`/api/hotels/{hotel_id}/local-attractions/{localAttraction_id}/`   |Update local-attractions (hotel staff)
  |**DELETE**       |`/api/hotels/{hotel_id}/local-attractions/{localAttraction_id}/`   |Delete local-attractions (hotel staff)

---

### Admin (staff only)
  |Method           |Path                                         |Function
  |-----------------|---------------------------------------------|---------|
  |**GET**          |`/api/hotels/{hotel_id}/admin/auth/`         |login  
  |**GET**          |`/api/hotels/{hotel_id}/admin/`              |admin panel 

## Notes
- The Hotel Management API is mainly for hotel owners/admins to manage listings, rooms, amenities, and media.


---

© 2025 GuzoMate Project Team
