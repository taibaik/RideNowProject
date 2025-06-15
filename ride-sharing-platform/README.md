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

🧱 System Overview

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
ride-sharing-platform/
├── user-service/
│   ├── main.py
│   └── routers/
│       └── user.py
│   └── services/
│       ├── db.py
│       ├── cache.py
│       └── auth.py
│
├── ride-service/
│   ├── main.py
│   └── routers/
│       └── ride.py
│   └── services/
│       ├── db.py
│       ├── cache.py
│       └── auth.py
│
├── payment-service/
│   ├── main.py
│   └── routers/
│       └── payment.py
│   └── services/
│       ├── db.py
│       ├── cache.py
│       └── auth.py
│
├── redis_cache.py
├── docker-compose.yml
└── README.md
```

---

## 🧪 Example Cache Usage

Redis is used to store recent queries (e.g., ride status). The `redis_cache.py` file contains utility functions:

```python
# redis_cache.py

import redis
import json

redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)
CACHE_TTL = 300  # seconds

def get_from_cache(key: str):
    value = redis_client.get(key)
    if value:
        return json.loads(value)
    return None

def set_cache(key: str, value: dict, ttl: int = CACHE_TTL):
    redis_client.set(key, json.dumps(value), ex=ttl)
```

---

## 📸 Screenshots

> _(Optional: Add screenshots of API testing or Postman results here if desired)_

---

## 📈 Future Improvements

- Add authentication tokens using JWT
- API Gateway for unified routing
- Frontend dashboard using React.js
- Integration with real payment API (e.g., Stripe)

---

## 📚 References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Redis Documentation](https://redis.io/)
- [PostgreSQL Documentation](https://www.postgresql.org/)
- [MongoDB Documentation](https://www.mongodb.com/docs/)

---

## 📝 License

MIT License © 2025 – Ride Sharing Team
