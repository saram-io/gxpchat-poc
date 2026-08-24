# GxPChat Phase 1 POC
Vercel AI SDK (chatbot UI only) + Pydantic AI (agent brain)

## Stack
- web/ : Next.js 14 + Vercel AI SDK `useChat` - pure UI, no logic
- agent/ : FastAPI + Pydantic AI - all GxP logic, tools, validation, audit

## Quick Start

### 1. Agent (Pydantic AI)
```bash
# from the repo root
python -m venv .venv && source .venv/bin/activate
pip install -r agent/requirements.txt
cp agent/.env.example agent/.env   # local Ollama by default; set MOCK_MODE=true for demos without Ollama
uvicorn agent.main:app --reload --port 8000
```

> Note: run as `agent.main:app` (package-style, so the relative imports resolve) — plain `main:app` fails with `ImportError`.

### 2. Web (Vercel AI SDK)
```bash
cd web
npm install
cp .env.example .env.local
npm run dev
Open http://localhost:3000
```

Flow: web useChat() -> /api/chat (Next.js) -> http://localhost:8000/agent/stream (FastAPI + Pydantic AI) -> streamed back

### 3. Full stack with Docker (agent + Ollama + Qdrant + Postgres)
```bash
cp agent/.env.example agent/.env   # compose overrides it with service names
docker compose up -d --build
```

Ports (remapped because 8000/6333/5432 are used by other stacks on this host):

| Service  | Host port | Notes |
|----------|-----------|-------|
| agent    | 8010      | FastAPI + Pydantic AI |
| ollama   | 11436     | GPU-enabled (RTX 4090), reuses host model store |
| qdrant   | 6335/6336 | REST / gRPC |
| postgres | 5434      | GxP audit store (future) |

Verify: `curl http://localhost:8010/` then POST to `/agent/run` or `/agent/stream`.

## GxP Validations in POC
- Pydantic schemas in agent/schemas.py are the validation specs
- Every answer must include CFRReference - enforced by Pydantic
- audit.py logs prompt, tool calls, model version, doc version for Part 11
- validation/eval_set.json = your PQ test harness (20 questions)
