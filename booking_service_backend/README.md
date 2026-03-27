# Hotel Booking Service (Core Backend)

A robust, asynchronous core backend service for a hotel booking system. Built with Clean Architecture principles, this project encapsulates complex business logic, concurrent background processing, and resilient database interactions, serving as a highly scalable foundation ready for API integration.

## 🚀 Key Architectural Features

* **Clean Architecture:** Strict separation of concerns across Models, Schemas, ORM layers, and Business Services to ensure high maintainability and testability.
* **Advanced Concurrency & Background Processing:** Custom async context managers (`BackgroundTaskObserver`) designed for the safe execution and graceful shutdown of non-blocking background tasks.
* **Resilient Transaction Management:** A robust `@transaction` decorator that ensures atomic database operations, automated connection pooling, and safe rollbacks during exceptions.
* **State Management Workers:** Autonomous background workers that continuously maintain system consistency (e.g., auto-clearing expired pending bookings and finalizing completed stays).
* **Modern Async ORM:** Fully asynchronous data access layer utilizing the latest SQLAlchemy 2.0 paradigms (`Mapped`, `mapped_column`) and `asyncpg`.

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python_3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy_2.0-D71F00?style=for-the-badge)
![Pydantic](https://img.shields.io/badge/Pydantic_V2-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![Asyncio](https://img.shields.io/badge/asyncio-000000?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)

* **Language:** Python 3.10+
* **Database:** PostgreSQL
* **Driver:** `asyncpg`
* **Data Validation:** Pydantic V2
* **Infrastructure:** Docker, Docker Compose

## 📁 Project Structure

```text
├── app/
│   ├── models/          # SQLAlchemy declarative models (Base, Hotels, Rooms, Bookings, Users)
│   ├── schemas/         # Pydantic models for strict data validation and DTOs
│   ├── orms/            # Database access layer (CRUD operations and complex async queries)
│   ├── services/        # Core business logic (BookingService, BackgroundProcesses)
│   ├── utils/           # Shared utilities (Custom Decorators, Task Observers, Paginators)
│   └── settings/        # Database connection and environment configuration
├── docker-compose.yml   # PostgreSQL container configuration
├── main.py              # Seed script demonstrating the asynchronous booking flow
├── requirements.txt     # Project dependencies
└── .env                 # Environment variables (needs to be created)

```
## ⚙️ Setup & Installation

### Prerequisites
* Python 3.10 or higher
* Docker and Docker Compose installed on your machine


### 1. Set up Environment Variables
Create a `.env` file in the root directory of the project and define the database credentials. Based on the `Settings` class, you need the following variables:

```env
DB_USER=your_postgres_user
DB_PASS=your_postgres_password
DB_NAME=your_database_name
DB_HOST=your_host
DB_PORT=your_port
```
*Note: The `docker-compose.yml` maps the container's PostgreSQL port to 5435 on your local machine to prevent conflicts with local database instances.*

### 2. Start the Database
Run the following command to start the PostgreSQL container in the background:

```bash
docker-compose up -d
```

### 3. Install Dependencies
Create a virtual environment and install the required Python packages:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

## 🏃‍♂️ Running the Application
Currently, the application runs as a demonstration script via `main.py`. This script initializes the database tables, executes the core transaction logic, and securely handles the simulated background approval process without blocking the event loop.

To run the demonstration script:

```bash
python main.py
```

## 🔮 Future Plans
* Integrate FastAPI to expose the core business logic via RESTful API endpoints.
* Implement JWT-based user authentication.
* Replace built-in async background tasks with a robust message broker (e.g., Redis + Celery/Taskiq) for production-grade worker scaling.