# 🧠 AIxplore Backend – Statue Recognition API using RAG (Flask + OpenAI)

**AIxplore** is an intelligent travel assistant that uses **RAG (Retrieval-Augmented Generation)** to identify and explain statues across England. This backend API, built with **Flask**, integrates user management, multimodal inputs (text, image, audio), geolocation, and AI-powered dialogue.

---

## 📦 Project Setup

### 1. Python Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

* Add your credentials in `key.pem`, `cert.pem`
* Configure OpenAI, Google Auth, database connection, etc., inside `application.py` or via `.env`

---

## 🚀 Running the Server

```bash
# Development
python application.py

# Production (via PM2)
pm2 start ecosystem.config.js
```

Log output is written to `app.log`, `app.log.1`, etc.

---

## 🌐 API Endpoints

### 🔐 Authentication & User Management

| Endpoint                | Method | Description                                   |
| ----------------------- | ------ | --------------------------------------------- |
| `/auth/google-signin`   | POST   | Sign in with Google and retrieve user info    |
| `/users/register`       | POST   | Register new user                             |
| `/users/update`         | POST   | Update user details (country, age, job, etc.) |
| `/users/reset_password` | POST   | Reset password                                |
| `/send_code`            | POST   | Send verification code to email               |
| `/verify_code`          | POST   | Verify email code                             |

---

### 💬 Chat (RAG-Based AI Conversations)

| Endpoint                      | Method | Description                                         |
| ----------------------------- | ------ | --------------------------------------------------- |
| `/v1/chat/completions`        | POST   | Main chat API — handles text, image, location input |
| `/v1/chat/classify_and_title` | POST   | Generate title and category for chat                |
| `/users/chats`                | GET    | Retrieve all chat history for current user          |
| `/users/chats/<chat_id>`      | DELETE | Delete specific chat                                |

> The chat system:
>
> * Accepts multimodal input
> * Uses location or content to identify a statue
> * Retrieves relevant data
> * Responds using OpenAI's GPT model

---

### 🎙️ Audio Transcription

| Endpoint            | Method | Description                              |
| ------------------- | ------ | ---------------------------------------- |
| `/transcribe_audio` | POST   | Convert uploaded audio to text (Whisper) |

---

## 🧠 Key Features

* ⚙️ **Flask + Flask-JWT-Extended** for routing and auth
* 📍 **Geolocation-aware responses** for contextual chat
* 🧠 **RAG with OpenAI GPT** for intelligent answers
* 🖼️ **Image upload support** to identify statues
* 🎧 **Audio input** via Whisper transcription
* 🛢️ **SQLAlchemy ORM** for managing users, chats, and POIs
* 📑 **Structured prompts** via YAML/JSON
* 🪵 **Robust logging** (`app.log`) and error handling

---

## 📁 Project Structure

```
AIxploreBackend/
├── application.py          # Flask app entry point
├── Database.py             # SQLAlchemy models
├── DatabaseManager.py      # DB operations wrapper
├── utils.py                # General utilities
├── prompts.yaml            # Predefined prompts for RAG
├── messages.json           # System message templates
├── uploads/                # Uploaded images and audio
├── templates/              # HTML templates (email etc.)
├── json/                   # Additional config/data
├── test_*.py               # Unit test files
├── key.pem / cert.pem      # SSL certificates
├── ecosystem.config.js     # PM2 process manager config
├── requirements.txt        # Python dependencies
├── app.log                 # Log files
└── venv/                   # Virtual environment
```



