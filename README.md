# 🚗 RideNow – Scalable Ride Sharing Platform

## 🧑‍💻 Team Members
- Muhammad Haiqal Dwikusuma – 22/496221/PA/21330  
- Kevin Beckham Hotama - 22/496130/PA/21308

---

## 📘 Project Overview
**RideNow** is a scalable microservices project that implements the core backend functionality of a ride-hailing application using FastAPI. The system is composed of two independent services:
-	User Service: Manages user-related operations, including registration and data management. Each user is assigned a unique identifier upon registration. 
-	Ride Service: Handles ride requests and manages the status of each ride throughout its lifecycle.
  
These services form the foundational backend of our ride-sharing application, developed with a focus on scalability, modularity, and maintainability. Performance is optimized using Redis caching, with each component fully containerized with Docker and communicating over RESTful APIs. 

---

## 🏗️ Architecture Highlights

### 🧱 System Overview

Our system consists of several independently scalable microservices:

🧍 User Service
-	Manages user registration and profile retrieval.
-	Assigns a unique ID to each user upon registration.
  
🚕 Ride Service
-	Handles ride creation and status management.
-	Each ride includes a driver and a status
  
💸 Payment Service
-	Simulates payment confirmation and transaction logging (Planned) 

## ⚙️ Infrastructure & Tooling
🧠 Redis Caching
- Used by both services to cache user and ride data.
- Reduces access time and improves response performance.
  
🛢️ Databases:
- MongoDB for User and Ride Services

🐳 Docker
- Each service is containerized and run using docker-compose

🔀 API Gateway / Reverse Proxy
- Optional future enhancement for unified routing.

Each service is containerized using Docker and orchestrated with `docker-compose`.

---

## 🔧 Tech Stack

| Layer             | Tech                     |
|------------------|--------------------------|
| Backend Framework| Python 3.10, FastAPI     |
| Database         | MongoDB                  |
| Caching          | Redis                    |
| Containerization | Docker, Docker Compose   |
| API Format       | RESTful JSON APIs        |

---

## ⚙️ How to Run Locally

### 1. Prerequisites
Make sure the following are installed:
- Docker
- Docker Compose

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/ride-sharing-platform.git
cd ride-sharing-platform
```

### 3. Run All Services with Docker Compose
This will spin up all services and dependencies (User, Ride, Redis, MongoDB):

```bash
docker-compose up --build
```
Expected running services:
- 🧍 User Service → http://localhost:8001
- 🚕 Ride Service → http://localhost:8002
- 🧠 Redis → localhost:6379
- 🛢️ MongoDB → localhost:27017

### 4. Test Services (Example with HTTPie or Curl)
Once the services are up, test endpoints using curl, httpie, or Postman.

#### Create a user
```bash
curl -X POST http://localhost:8001/users \
  -H "Content-Type: application/json" \
  -d '{"id": "u001", "name": "Kevin", "role": "rider"}'
```

#### Get a user
```bash
curl http://localhost:8001/users/u001
```

#### Create a ride
```bash
curl -X POST http://localhost:8002/rides \
  -H "Content-Type: application/json" \
  -d '{"id": "r123", "driver": "Dewi", "status": "pending"}'
```

#### Get a ride
```bash
curl http://localhost:8002/rides/r123
```

### 5. (Optional) 🛠️ Manual Dev Mode 
To run a service manually (without Docker):

```bash
cd user-service  # or ride-service
uvicorn main:app --reload --port 8001  # or 8002 for Ride
```
Ensure MongoDB and Redis are running locally or update their connection URIs in the code.

## 📁 Project Structure

```
ridenowproject
├── ride-service/
│   ├── main.py                    # Entry point for ride service
│   ├── Dockerfile                 # Docker config for ride service
│   ├── redis_cache.py             # Redis cache logic
│   ├── services/
│   │   └── mongodb.py             # MongoDB connection logic
│   └── __pycache__/               # Compiled Python bytecode
│       ├── main.cpython-310.pyc
│       └── redis_cache.cpython-310.pyc
│
├── user-service/
│   ├── Dockerfile                 # Docker config for user service
│   ├── main.py                    # Entry point for user service
│   ├── redis_cache.py             # Redis cache logic
│   └── services/
│       └── mongodb.py             # MongoDB connection logic
│
├── docker-compose.yml             # Docker Compose configuration
├── README.md                      # Project documentation
└── desktop.ini                    # Local fallback config (used if Docker fails to run)
```

---
## 🔑 API Endpoints
### User Service (http://localhost:8001)
| Method | Endpoint           | Description           |
| ------ | ------------------ | --------------------- |
| POST   | `/users`           | Register a new user   |
| GET    | `/users/{user_id}` | Retrieve user details |

Example Request:
```bash
curl -X POST http://localhost:8001/users \
  -H "Content-Type: application/json" \
  -d '{"id": "u001", "name": "Kevin", "role": "rider"}'
```

### 🚕 Ride Service (http://localhost:8002)
| Method | Endpoint           | Description               |
| ------ | ------------------ | ------------------------- |
| POST   | `/rides`           | Create a new ride         |
| GET    | `/rides/{ride_id}` | Retrieve ride information |

Example Request:
```bash
curl -X POST http://localhost:8002/rides \
  -H "Content-Type: application/json" \
  -d '{"id": "r123", "driver": "Dewi", "status": "pending"}'
```
📌 All endpoints return JSON responses and leverage Redis caching for fast repeat lookups.

---

## 🧠 Redis Caching
To optimize performance and reduce database load, Redis is used as a caching layer across both the **User Service** and **Ride Service**.

✅ How It Works
- When a user or ride is retrieved, the service first checks Redis for cached data.
- If the data exists in Redis:
  - It returns immediately (faster than querying MongoDB)
  - A message is logged to indicate a cache hit
- If the data is not in cache, it is fetched from MongoDB and then stored in Redis for future   requests.

### 🧾 Cache Utility – redis_cache.py
```python
import redis, json

redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)
CACHE_TTL = 300  # cache timeout in seconds (5 minutes)

def get_from_cache(key: str):
    value = redis_client.get(key)
    return json.loads(value) if value else None

def set_cache(key: str, value: dict, ttl: int = CACHE_TTL):
    print(f"SET CACHE: {key} = {value}")
    redis_client.set(key, json.dumps(value), ex=ttl)
```

### 💡 Example Keys
- user:u001 → Cached user with ID u001
- ride:r123 → Cached ride with ID r123
  
This design helps the app scale better under load by avoiding repeated database queries for frequently accessed resources.

---

## 📈 Future Improvements
While the current implementation provides a functional microservice-based ride-hailing backend, several improvements are planned to make the system more robust, secure, and production-ready:

🧱 Backend Improvements
- Add proper indexing for faster ride/user lookup
- Support pagination and filtering in GET endpoints

🔐 Security & Authentication
- Implement JWT-based authentication for users
- Add role-based access control (e.g., rider vs driver vs admin)
- Secure endpoints with middleware and token verification

💸 Payment Service
- Add a dedicated payment microservice
- Simulate payment confirmation and store transactions in PostgreSQL
- Handle payment status updates on ride completion

🌐 API Gateway
- Introduce an API gateway (e.g., Traefik or NGINX) for unified routing
- Add logging, throttling, and centralized auth handling

📊 Monitoring & DevOps
- Integrate Prometheus + Grafana for service-level monitoring
- Add structured logging and tracing (e.g., OpenTelemetry)
- Add CI/CD pipelines using GitHub Actions or GitLab CI

💻 Frontend Application
- Build a simple frontend in React or Flutter
- Enable users to register, request rides, and track their history
- Provide a responsive mobile-friendly UI

---
## 💻 Development Experience
✅ What We Learned
- **Microservices Architecture**
  Learned to design independent, modular services with clearly defined responsibilities and communication via REST APIs.
- **FastAPI for Rapid API Development**
  Used FastAPI to quickly build asynchronous APIs with automatic validation and documentation.
- **Redis Caching Principles**
  Integrated Redis to reduce database load and improve performance for repeat queries.
- **MongoDB & Async Operations with Motor**
  Used Motor (async MongoDB driver) to support non-blocking data access in Python services.
- **Containerization with Docker**
  Containerized all services for easier orchestration, environment consistency, and testing.

**Real Challenges We Faced**
- **Service Dependency Order**
  Some services failed to start because Redis or MongoDB weren’t ready yet. We solved this using `depends_on` and retry logic.
- **Async DB Handling**
  Using Motor required changing how we read/write data. Handling `_id` fields and async logic was tricky at first.
- **Redis Serialization**
  Redis stores only strings, so we had to manually `json.dumps()` data before storing and `json.loads()` when retrieving.
- **In-Memory vs Persistent State**
  Initially used fake dictionaries to simulate databases. Switching to MongoDB solved issues with data persistence after restarts.
- **Cache Expiry Strategy**
  Choosing TTL values and invalidation logic for cached objects like users and rides required thoughtful balancing.
- **REST API Design**
  Ensured all endpoints followed consistent naming, request/response formats, and proper status code usage.

---

## 📚 References

- FastAPI Documentation: https://fastapi.tiangolo.com/
- MongoDB Documentation: https://www.mongodb.com/docs/
- Redis Documentation: https://redis.io/docs/
- Docker Documentation: https://docs.docker.com/
- Uvicorn Documentation: https://www.uvicorn.org/
- Pydantic Documentation: https://docs.pydantic.dev/
- Motor (Async MongoDB Driver): https://motor.readthedocs.io/

---
  
Build using SCALABLE Microservices Architecture 
© 2025 – Ride Sharing Team
