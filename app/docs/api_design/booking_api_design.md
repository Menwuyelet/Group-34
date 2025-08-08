# GuzoMate – API Design Documentation (Booking and listing service)

This document provides the API design for the booking and listing services in the GuzoMate project.

- **Booking and Listing api** — manages hotel listings, reservations, reviews and ratings, guest, and related entities.


---

### Hotels

  |Method          |Path                                       |Function
  |----------------|-------------------------------------------|---------|
  |**GET**         |`/api/hotels/`                             |List hotels  
  |**GET**         |`/api/hotels/{hotel_id}/`                  |Hotel details  
  |**POST**        |`/api/hotels/`                             |Create hotel (Site admin only)    
  |**DELETE**      |`/api/hotels/{hotel_id}/`                  |Delete hotel (Site admin only)
  |**PUT**         |`/api/hotels/{hotel_id}/`                  |Update hotel (Site admin only)
  |**GET**         |`/api/hotels/{hotel_id}/rooms/`            |Room list for hotel  
  |**GET**         |`/api/hotels/rooms/{room_id}/`             |Room detail for hotel  

---

### Guests(Authenticated user)

  |Method           |Path                                       |Function
  |-----------------|-------------------------------------------|---------|
  |**GET**          |`/api/users/`                              |List users (Site admin only) 
  |**GET**          |`/api/users/{user_id}/`                    |Get user 
  |**GET**          |`/api/users/{user_id}/profile`             |Get user profile 
  |**PUT**          |`/api/users/{user_id}/profile`             |update user profile
  |**DELETE**       |`/api/users/{user_id}/`                    |Delete user

---

### Reservations(Authenticated user)

  |Method           |Path                                              |Function
  |-----------------|--------------------------------------------------|---------|
  |**GET**          |`/api/reservations/{user_id}/`                    |Reservations by guest
  |**GET**          |`/api/reservations/{user_id}/{reservation_id}/`   |Reservation details
  |**POST**         |`/api/reservations/{user_id}/`                    |Create new reservation
  |**PUT**          |`/api/reservations/{user_id}/{reservation_id}/`   |Update reservation status
  |**DELETE**       |`/api/reservations/{user_id}/{reservation_id}/`   |Delete reservation
  |**GET**          |`/api/reservations/{hotel_id}/`                   |Reservations by hotel (Site admin only) 

---

### Reviews(Authenticated user)

  |Method           |Path                                        |Function
  |-----------------|--------------------------------------------|---------|
  |**POST**         |`/api/reviews/`                             |Create review 
  |**PUT**          |`/api/review/{review_id}/`                  |Review details  
  |**DELETE**       |`/api/review/{review_id}/`                  |Delete review (owner and site admin only)
  |**GET**          |`/api/reviews/{hotel_id}/`                  |Reviews for hotel

---

### Favorites(Authenticated user)

  |Method           |Path                                        |Function
  |-----------------|--------------------------------------------|---------|
  |**GET**          |`/api/favorites/{profile_id}`               |List favorites
  |**POST**         |`/api/favorites/{profile_id}`               |Add favorite hotel  
  |**DELETE**       |`/api/favorites/{profile_id}/{fav_id}/`     |Remove favorite   

---

### History(Authenticated user)

  |Method           |Path                                        |Function
  |-----------------|--------------------------------------------|---------|
  |**GET**          |`/api/history/{profile_id}/`                |Reservation history for profile  
  |**DELETE**       |`/api/history/{profile_id}/{history_id}`    |Remove reservation history  

---

### Cities

  |Method           |Path                        |Function
  |-----------------|----------------------------|---------|
  |**GET**          |`/api/cities/`              |List cities   
  |**POST**         |`/api/cities/`              |Post city (Site admin) 
  |**PUT**          |`/api/cities/{city_id}/`    |Update city (Site admin)  
  |**GET**          |`/api/cities/{city_id}/`    |City detail
  |**DELETE**       |`/api/cities/{city_id}/`    |City details  

---

## Notes
- The Hotel Management API is mainly for users and site admin to access listings, reservations, reviews, ratings and other related data.

---

© 2025 GuzoMate Project Team

