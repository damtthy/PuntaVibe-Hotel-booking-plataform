# 🏨 Punta Vibe - Boutique Hotel Booking System

Welcome to **Punta Vibe**, an exclusive boutique hotel booking and management system inspired by seasonal luxury destinations like Punta del Este. This application was built from the ground up as a **Full Stack Developer Master's Capstone Project**.

The primary goal is to solve a real-world business problem through a robust, efficient, and scalable **MVP (Minimum Viable Product)**. The system allows users to search for room availability, dynamically calculate pricing based on seasons/occupancy, and seamlessly manage bookings.

---

## 👤 Author
* **Developer:** Thiago Sabatoni
* **Program:** Master in Full Stack Development

---

## 🛠️ Tech Stack

The architecture is cleanly divided into Backend and Frontend layers to follow modern industry standards:

* **Backend (Logic & API):**
  * **Python** with **Django** / **Django REST Framework** (DRF) for building a secure RESTful API.
  * Relational Database (**PostgreSQL** / **SQLite** for development) designed for optimal data integrity.
* **Frontend (User Interface):**
  * **React** featuring modern, interactive components.
  * Structured styling for a smooth, mobile-responsive User Experience (UX).
* **DevOps & Version Control:**
  * **Git** and **GitHub** for version control and repository management.

---

## 📊 Data Architecture & Models

The database structure relies on 4 core interconnected entities ("models") to handle the business operations:

1. **User Model:** Inherits from Django's native authentication system to support three strict roles:
   * *Anonymous Visitor:* Can browse the catalog, view standard availability, and check rates.
   * *Registered Customer:* Authenticated user allowed to book rooms and view booking history.
   * *Administrator (Manager):* Full system access to manage suites, configure pricing rules, and track revenue.
2. **Suite Model:** Represents the hotel's premium rooms. Contains the suite name, description, capacity, and a **base price of 150 USD** per night.
3. **Season Model (`Season`):** Defines calendar ranges (High, Mid, Low seasons) mapped to specific start/end dates and their respective **price multipliers**.
4. **Booking Model (`Booking`):** The core transaction model. Links a User to a specific Suite for a designated Check-in/Check-out range, automatically calculating the total amount charged.

---

## 💸 Business Rules (Dynamic Pricing Logic)

To maximize revenue and optimize occupancy trends, the backend automatically calculates rates based on the following rules:
* **Base Rate:** Every standard suite starts at **150 USD** per night.
* **Seasonal Adjustment:** Nightly rates automatically scale based on the active season multiplier (e.g., High Season = 1.5x multiplier).
* **Occupancy-Based Dynamic Pricing:**
  * **Low Occupancy Discount (Demand Booster):** If total hotel occupancy for the selected dates is high/empty (e.g., more than 70% of suites are available), the system applies a **10% discount** to incentivize new bookings and reduce vacancy.
  * **High Occupancy Surge (Dynamic Pricing):** If availability drops below critical thresholds due to high demand, price surges trigger automatically:
    * Less than 30% availability: +20% price increase.
    * Less than 10% availability: +40% price increase.
* **Server-Side Security:** All mathematical calculations and availability checks run strictly on the backend to prevent front-end tampering.

---

## 🚀 Development Roadmap

Following an agile approach, the project execution is split into the following phases:
1. **Phase 1:** Environment setup and Database Modeling (Django Models).
2. **Phase 2:** Core Backend development (API Endpoints & Authentication).
3. **Phase 3:** Frontend implementation (React Catalogs & Booking Forms).
4. **Phase 4:** Full integration, dynamic edge-case testing, and Cloud Deployment.# PuntaVibe-Hotel-booking-plataform
