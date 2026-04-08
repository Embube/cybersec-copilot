# CyberSec Copilot Enterprise

A full-stack cybersecurity demo platform with:

- FastAPI backend
- React + Vite frontend
- JWT authentication
- SQLite + SQLAlchemy persistence
- Incident CRUD + comments
- Dashboard metrics
- AI triage endpoint
- Document library metadata
- Docker support
- GitHub Actions CI
- Azure deploy workflow template

## Important notes

This is a **real runnable starter system** with a production-style structure.

What is fully implemented:
- user registration/login
- JWT bearer auth
- incidents, comments, documents metadata
- live dashboard metrics
- React dashboard pages
- Docker and CI skeletons

What is intentionally left configurable:
- OpenAI key for real AI triage
- PDF/RAG ingestion pipeline (scaffold included, not full embedding stack)
- n8n/ServiceNow/Jira integrations (stubs included)
- Azure deployment values

## Quick start

### Backend

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env   # Windows
# cp .env.example .env   # macOS/Linux

uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Backend: http://127.0.0.1:8000  
Frontend: http://127.0.0.1:5173  
API docs: http://127.0.0.1:8000/docs

## Demo flow

1. Register a user in Swagger or from the Login page.
2. Log in to get a JWT token.
3. Create incidents from the frontend or `/api/incidents`.
4. View dashboard metrics and incident charts.
5. Add comments to incidents.
6. Use `/api/ai/triage` to simulate or run real AI alert triage.

## Default environment variables

See `.env.example`.

## Docker

```bash
docker compose up --build
```

## Repo structure

```text
app/
  api/
  core/
  db/
  models/
  schemas/
  services/
  integrations/
frontend/
  src/
.github/workflows/
```
