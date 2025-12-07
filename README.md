
# 🛡️ AI Backend System - Microservices Fraud Detection

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95%2B-009688?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

## 📖 Overview

This project is a robust **Microservices Architecture** designed to simulate a real-world **Fraud Detection System**. It orchestrates multiple independent services to process transactions, predict fraudulent activity using Machine Learning, and handle logging/alerting asynchronously.

The system demonstrates modern backend practices including **asynchronous service-to-service communication**, **JWT authentication**, and **centralized logging** with S3 integration.

---

## 🏗️ Architecture

The system is composed of 5 distinct microservices communicating via HTTP (REST APIs):

| Service | Port | Description |
| :--- | :--- | :--- |
| **🧠 AI Service** | `:8000` | The core "brain". Orchestrates the prediction flow, fetches GeoIP data, runs the ML model, and triggers alerts/logs. |
| **👤 User Service** | `:8001` | Manages user registration, login, and **JWT Authentication**. |
| **🚨 Alert Service** | `:8003` | Handles critical notifications (e.g., sending emails to admins when fraud is detected). |
| **📝 Log Service** | `:8004` | Centralized auditing service that archives logs to AWS S3 (or compatible storage). |
| **🌍 External API** | `:8005` | Simulates external third-party APIs (e.g., GeoIP location services) to enrich transaction data. |

### 🔄 Workflow Example: Fraud Prediction

1.  **Request:** Client sends transaction data to the `AI Service`.
2.  **Enrichment:** AI Service asynchronously fetches location data from the `External API Service`.
3.  **Prediction:** The Scikit-Learn model analyzes features (Amount, Transaction Type, Location, etc.).
4.  **Action:**
    * **Parallel Execution:** Using `asyncio.gather`, the system simultaneously:
        * Sends a notification to the `Alert Service` (if fraud is probable).
        * Archives the transaction details in the `Log Service`.
5.  **Response:** Returns the fraud probability and status to the client.

---

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Framework:** FastAPI (High performance async framework)
* **Machine Learning:** Scikit-Learn, Joblib, Numpy
* **Authentication:** JWT (JSON Web Tokens) with `python-jose`
* **Communication:** `httpx` (Async HTTP client)
* **Database/Storage:** SQLAlchemy (SQLite/PostgreSQL), AWS S3 (Logging)
* **Deployment:** Docker & Docker Compose

---

## 📂 Project Structure

```bash
├── ai_service/             # ML Model & Prediction Logic
│   ├── app/services/       # Prediction Service & GeoIP Integration
│   └── model_files/        # Serialized Scikit-learn models (.pkl)
├── user_service/           # Auth & User Management
│   ├── app/services/       # JWT Handling & User CRUD
│   └── database/           # DB Connection
├── alert_service/          # Notification System
├── log_service/            # S3 Logging Integration
└── external_apis_services/ # Mock External Providers (Location/GeoIP)
