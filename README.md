# Project Overview
DeployForge is a backend system that simulates how modern platforms like Vercel or Railway handle deployments. It uses a microservices architecture and asynchronous processing to handle deployment tasks efficiently.

# 🚀 DeployForge

A microservices-based deployment platform that allows users to deploy GitHub repositories asynchronously using FastAPI, Celery, Redis, and MongoDB.

---

## 📌 Features

- 🔥 Deploy GitHub repositories via API
- ⚡ Asynchronous processing using Celery + Redis
- 📦 Automatic repository cloning
- 📊 Deployment status tracking (queued, cloned, failed)
- 📄 View all deployments
- ❌ Delete deployments
- 🛡️ Error handling for invalid repositories

---



## 🏗️ Architecture
```text
User
↓
API Gateway (FastAPI)
↓
Orchestrator (FastAPI)
↓
Redis (Message Broker)
↓
Celery Worker
↓
Git Clone
↓
MongoDB
```

### Current Services

- API Gateway
- Orchestrator
- Celery Worker
- Redis
- MongoDB

### Planned Services

- Docker Manager
- Log Service
- Frontend Dashboard

---

## 🧠 Tech Stack

- **Backend:** FastAPI (Python)
- **Queue System:** Celery
- **Message Broker:** Redis
- **Database:** MongoDB
- **Version Control:** GitPython
- **Async HTTP Client:** httpx

---

## 🚀 API Endpoints

### 1. Deploy Repository

```http
POST /deploy
```

**Request Body:**
```json
{
  "repo_url": "https://github.com/user/repo.git"
}
```

**Response:**
```json
{
  "deployment_id": "uuid",
  "status": "queued",
  "message": "Deployment started"
}
```

---

### 2. Get All Deployments

```http
GET /deployments
```

**Response:**
```json
[
  {
    "deployment_id": "...",
    "repo_url": "...",
    "status": "cloned"
  }
]
```

---

### 3. Delete Deployment

```http
DELETE /deployment/{deployment_id}
```

**Response:**
```json
{
  "status": "success",
  "message": "Deployment deleted successfully"
}
```

# 🔄 Deployment Lifecycle
queued → cloned ✅
       → failed ❌

# 🛡️ Error Handling

Invalid repository → marked as failed

Empty input → 422 validation error

Orchestrator down → handled gracefully

# ⚙️ Setup Instructions
1. Clone Repository
git clone https://github.com/your-username/DeployForge.git
cd DeployForge
2. Install Dependencies
pip install -r requirements.txt
3. Start Services
🔹 Start Redis (Docker)
docker run -d -p 6379:6379 redis
🔹 Start MongoDB (Docker)
docker run -d -p 27017:27017 --name mongodb mongo
4. Run API Gateway
cd api-gateway
uvicorn app.main:app --reload --port 8000
5. Run Orchestrator
cd orchestrator
uvicorn app.main:app --reload --port 8001
6. Run Celery Worker
celery -A app.tasks worker --loglevel=info --pool=solo

# 🧪 Testing

Swagger UI: http://127.0.0.1:8000/docs

Use Postman or curl for API testing

# 💡 Future Improvements

🐳 Docker container deployment

📊 Real-time logs streaming

🧹 Hard delete (remove files + DB)

🔄 Retry mechanism for failed deployments

🌐 Frontend dashboard

## 📚 Key Learnings

- Designed microservices-based architecture
- Implemented asynchronous task processing using Celery
- Integrated Redis as a message broker
- Handled failure scenarios and state tracking
- Built RESTful APIs for deployment lifecycle management

## 👩‍💻 Author
*Manvi*
