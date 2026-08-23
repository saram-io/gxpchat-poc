# GxPChat Phase 1 POC
Vercel AI SDK (chatbot UI only) + Pydantic AI (agent brain)

## Stack
- web/ : Next.js 14 + Vercel AI SDK `useChat` - pure UI, no logic
- agent/ : FastAPI + Pydantic AI - all GxP logic, tools, validation, audit

## Quick Start

### 1. Agent (Pydantic AI)
cd agent
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # local Ollama by default; set MOCK_MODE=true for demos without Ollama
uvicorn main:app --reload --port 8000

### 2. Web (Vercel AI SDK)
cd web
npm install
cp .env.example .env.local
npm run dev
Open http://localhost:3000

Flow: web useChat() -> /api/chat (Next.js) -> http://localhost:8000/agent/stream (FastAPI + Pydantic AI) -> streamed back

## GxP Validations in POC
- Pydantic schemas in agent/schemas.py are the validation specs
- Every answer must include CFRReference - enforced by Pydantic
- audit.py logs prompt, tool calls, model version, doc version for Part 11
- validation/eval_set.json = your PQ test harness (20 questions)
