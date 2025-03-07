# 🧙‍♂️ Hermeticum

**Hermeticum** is an **AI-powered tarot journaling platform** designed to help users **record insights, track ideas, and explore patterns in their thoughts**.

It combines structured journaling with AI-guided reflection, offering **tarot deck integrations and spread analysis** for self-discovery and creative insight.

---

## ✨ Features

- 🔮 **AI-Powered Tarot Journaling** — Snap a picture of your spread, and the AI helps recognize the cards and refine interpretations.
- 📝 **Interactive Journal Entries** — Log readings, insights, and thoughts in a structured, easily searchable format.
- 🤖 **Smart AI Feedback** — AI-assisted journaling suggestions based on previous entries.
- 📊 **Idea Mapping & Trends** — Visualize connections between journal entries over time.
- 📱 **Multi-Platform** — Accessible as a **web app and mobile companion app** in the future.

---

## 🏗️ Tech Stack

### 🔹 Backend
- **FastAPI** — High-performance API framework (Python)
- **PostgreSQL** — Relational database for journal entries & user data
- **SQLAlchemy & Alembic** — ORM & migrations
- **Docker** — Containerized microservices
- **Uvicorn** — ASGI server for FastAPI
- **Firebase Authentication** — Secure user auth
- **Celery (Future)** — For background tasks (e.g., AI processing)

### 🔹 Frontend
- **React + TypeScript** — Component-based UI
- **Vite** — Fast development tooling
- **Tailwind CSS** — Responsive styling
- **React Router** — Client-side routing

### 🔹 AI & ML
- **OpenAI API** — AI-generated insights and journaling nudges
- **Machine Vision (Future)** — Detect tarot spreads from images
- **LLM Fine-Tuning (Future)** — Personalized journaling assistant

### 🔹 DevOps & Infrastructure
- **Docker & Docker Compose** — Containerized deployment
- **Colima (for macOS users)** — Lightweight container runtime
- **CI/CD (Planned)** — GitHub Actions for automated deployments

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/yourusername/hermeticum.git
cd hermeticum
