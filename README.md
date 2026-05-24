# Signature - Autonomous AI Business Operating System

An AI-powered business operating system that allows founders and teams to run entire companies from one intelligent dashboard using coordinated AI agents.

## Overview

Signature combines autonomous workflows, operational intelligence, AI coding automation, marketing automation, finance tracking, research systems, and centralized orchestration into a single interface.

## Project Structure

```
Signature/
├── backend/              # FastAPI backend
│   └── app/
│       ├── api/          # API endpoints
│       ├── agents/       # AI agent implementations
│       ├── core/         # Core business logic
│       ├── models/       # Database models
│       ├── schemas/      # Pydantic schemas
│       ├── services/     # Business services
│       └── utils/        # Utility functions
├── frontend/             # Next.js frontend
│   ├── pages/            # Next.js pages
│   ├── components/       # React components
│   ├── styles/           # CSS/Tailwind styles
│   ├── utils/            # Utility functions
│   ├── lib/              # Library code
│   └── public/           # Static assets
└── docker/               # Docker configuration
```

## Getting Started

### Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Setup
```bash
cd frontend
npm install
```

### Development
```bash
# Backend
cd backend
uvicorn app.main:app --reload

# Frontend
cd frontend
npm run dev
```

## Core Features

- Orchestrator Agent (central coordinator)
- Planning Agent (strategy and roadmap)
- Code Agent (AI-powered development)
- Finance Agent (PayPal tracking, analytics)
- Social Posts Agent (content generation)
- Email Outreach Agent (lead nurturing)
- Support Reply Agent (customer service)
- Ads Agent (campaign management)
- Competitor Research Agent (market intelligence)
- Memory System (ChromaDB)
- Approval Workflows
- Task Scheduling (Celery/Redis)
- Dashboard Interface

## Technologies

- Backend: FastAPI, SQLAlchemy, Celery, Redis, PostgreSQL
- Frontend: Next.js, TypeScript, Tailwind CSS, shadcn/ui
- Memory: ChromaDB
- AI Runtime: Claude Code CLI
- Infrastructure: Docker Compose, nginx

## License

MIT