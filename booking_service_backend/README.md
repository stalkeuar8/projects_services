# 🏨 Booking System API

High-performance asynchronous booking system built with FastAPI, PostgreSQL, and Docker.
Designed with clean architecture principles and optimized for concurrency and scalability.

---

## 🚀 Features

* 🔐 JWT Authentication (Access + Refresh tokens)
* 🏨 Room booking system with availability checks
* 🤖 Telegram bot integration for booking approvals
* 📊 Booking statistics & management
* ⚡ Fully asynchronous (FastAPI + Async SQLAlchemy)
* 🐳 Dockerized setup (one command запуск)
* 🔄 Transaction-safe booking logic
* 🧠 Clean architecture (API / Service / Repository)

---

## ⚙️ Performance

> Optimized FastAPI to handle **400+ concurrent users** and **120+ RPS**
> by implementing:

* Database indexing
* Connection pool tuning
* Efficient async queries

---

## 🧱 Tech Stack

### Backend

![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge\&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge\&logo=python)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red?style=for-the-badge)

### Database & Cache

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-316192?style=for-the-badge\&logo=postgresql)
![Redis](https://img.shields.io/badge/Redis-Cache-red?style=for-the-badge\&logo=redis)

### Async & Integrations

![Aiogram](https://img.shields.io/badge/Aiogram-Telegram-blue?style=for-the-badge)
![Aiohttp](https://img.shields.io/badge/Aiohttp-Async-green?style=for-the-badge)

### DevOps

![Docker](https://img.shields.io/badge/Docker-Containerization-2496ED?style=for-the-badge\&logo=docker)

---

## 🧠 System Design

The system follows a layered architecture:

```
API Layer → Service Layer → Repository Layer → Database
```

### 🔹 API Layer

* Handles HTTP requests
* Validates input data
* Delegates logic to services

### 🔹 Service Layer

* Contains business logic
* Coordinates multiple repositories
* Ensures transactional consistency

### 🔹 Repository Layer

* Works directly with the database
* Encapsulates SQLAlchemy queries

---

## 🔒 Booking Flow

1. User sends booking request
2. System starts a database transaction
3. Target room is locked (`SELECT FOR UPDATE`)
4. Availability is checked
5. Booking is created if valid
6. Transaction is committed
7. Telegram bot receives approval request
8. User gets confirmation

👉 This guarantees:

* No race conditions
* Strong consistency
* Safe concurrent booking handling

---

## 🔐 Authentication Flow

* Access token (short-lived)
* Refresh token (long-lived)
* Redis blacklist for revoked tokens

---

## 📦 Project Structure

```
app/
 ├── api/
 ├── services/
 ├── repositories/
 ├── models/
 ├── schemas/
 ├── core/
 └── bot/
```

---

## 🐳 Getting Started

### 1. Clone repository

```bash
git clone https://github.com/your-username/your-project.git
cd your-project
```

---

### 2. Create environment file

```bash
cp .env.example .env
```

Fill in required variables:

* DB credentials
* JWT secret
* Redis URL
* Telegram bot token

---

### 3. Run with Docker

```bash
docker-compose up --build
```

---

### 4. Access the app

* API: http://localhost:8000
* Docs: http://localhost:8000/docs

---

## 🧪 Running Tests (optional)

```bash
pytest
```

---

## 📈 Future Improvements

* Background jobs (Celery / Redis queue)
* Rate limiting
* Caching layer
* Advanced monitoring (Prometheus)

---