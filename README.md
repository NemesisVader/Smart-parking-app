# 🚗 Vehicle Parking App - V1

**A Flask-based web application to manage 4-wheeler parking lots with separate roles for Admin and Users. Built as part of the Modern Application Development I course at IIT Madras.**

---

## 📌 Project Overview

This application allows:
- **Admins** to manage parking lots and spots
- **Users** to register, reserve and release parking spots
- **Reservations** to be tracked with timestamps and cost calculations

The application is designed to run locally using Flask, SQLite, and Bootstrap, following an MVC-style architecture.

---

## 👨‍💻 Roles and Functionalities

### 🔐 Admin (Superuser)
- Create/Edit/Delete Parking Lots
- Automatically generate parking spots when creating a lot
- View spot statuses: Available, Reserved, Occupied
- View all users and their reservation history
- Dashboard summary with charts/statistics

### 👥 User
- Register/Login securely
- Reserve a parking spot (auto-assigned)
- Release a spot and get cost summary
- View reservation history and charts

---

## 🛠️ Tech Stack

| Layer       | Technology                       |
|-------------|----------------------------------|
| Backend     | Python, Flask                    |
| Frontend    | Jinja2, HTML, CSS, Bootstrap     |
| Database    | SQLite                           |
| Extensions  | Flask-Login, Chart.js (optional) |

---

## 🗃️ Database Schema

### Tables:
- `users`: user info, roles
- `parking_lots`: location, rate, total spots
- `parking_spots`: status and lot association
- `reservations`: timestamps, pricing, user-spot relation
