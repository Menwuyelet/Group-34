#  GuzoMate – Hotel Listing, Rating, and Booking Platform

## Overview

**Project Name:** GuzoMate

**Sector:**  Hospitality and Tourism Technology

**Purpose:** To provide a centralized digital platform for listing, reviewing, Booking, and promoting hotels in Ethiopia.

This project is designed for local and international travelers looking to explore Ethiopia. It helps them discover and access hotels across the country and enables hotel businesses to promote their services online.

---

## Problem Statement

- Lack of a centralized local platform for hotel listing and booking across Ethiopia.
- Limited access to structured and reliable information for travelers.
- Minimal digital presence for many hospitality(hotel) businesses in Ethiopia.

---

# Solution
## GuzoMate addresses these issues by:
- Offering a unified platform where users can browse, review, and book hotels nationwide.
- Providing hotels with tools to manage their profiles, availability, and promotions digitally.
- Supporting multilingual interfaces and multiple currencies to serve both local and international users.
- Integrating a dedicated microservice for hotel data and booking management to ensure scalability and reliability.

## Goals

- Create a centralized platform for hotel listing and booking in Ethiopia.
- Provide tourists(local and international) with reliable hotel information, reviews, and ratings.
- Empower hospitality(hotel) businesses with tools to promote their services.
- Promote tourism, cultural exchange, and better travel planning.
- To provide a digital booking Management platform for hotels.

---

## Target Audience / Beneficiaries
- Local and international travelers visiting Ethiopia.
- Ethiopian hotel businesses seeking digital promotion and booking management.
- Tourism stakeholders looking to improve visitor experience.
- The broader community benefiting from increased tourism and cultural exchange.

## Key Features

- **Hotel Listing, Searching and Booking:** Filterable/searchable listings of hotels.
- **Hotel Reviews and Ratings:** User-generated content to inform others.
- **Environmental Guides:** Information about surroundings and attractions.
- **Promotional Tools for Hotels:** Allow hotel businesses to manage and promote their profiles.
- **Multilingual Support:** Support for English, Amharic, and potentially more.
- **Multiple Currencies:** including ETB-based(local currency) pricing and transactions.
- **Booking Management** For hotels to manage all types of bookings both online and in person.
- **Microservice Integration:** A dedicated Hotel Management API handles hotel CRUD and availability via internal HTTP communication.

---

## System Architecture

- **Architecture Type:** Three-Tier Web Architecture + Microservice Integration

### Technology Stack

- **Frontend:** React.js
- **Backend (API & Business Logic):** Django (REST API)
- **Database:** PostgreSQL
- **Hosting:** Cloud or containerized infrastructure (TBD)

### Three-Tier Architecture

1. **Presentation Tier (Frontend)**

   - Built with React.
   - User interfaces for guests and hotel owners.
   - Features: hotel browsing, reviews, maps, ratings, booking and hotel dashboard.

2. **Logic Tier (Backend)**

   - Built with Django REST Framework.
   - Handles user authentication, business rules, data processing, and API endpoints.
   **Responsibilities:**
      - API endpoints for reviews, booking, user authentication
      - HTTP communication with a separate Hotel Management API

3. **Data Tier (Database)**
   - PostgreSQL for both the booking and management api.
   - Stores hotel data, user profiles, reviews, etc.

---

## Microservice Integration

- The **Main Backend** communicates with the **Hotel Management API** using secure HTTP requests.
- The **Hotel API** is a separate Django service responsible for:
   - Hotel and room data
   - Availability management
   - hotel dashboard and profile control

## Impact

- Improves the tourism experience in Ethiopia.
- Encourages local hospitality(hotel) businesses to adopt digital solutions.
- Establishes GuzoMate as Ethiopia’s digital tourism gateway.
- Promotes cultural heritage and eco-tourism awareness.

---

## Future Enhancements(long term plans)
- payment integrations
- Integration with Transport and Travel Agencies
- AI-powered recommendation engine
- Mobile application (Android/iOS)

---

## Contributors

- Menwuyelet Temesgen – Backend developer
- Dawit Solomon - Fullstack developer
- Stephen Pakateng - Frontend developer
- Amen Adane - Fullstack developer
- Kang Malual- Frontend developer

---

© 2025 GuzoMate Project Team
