# Project instructions

Follow the ponytail skill: write only what the task needs, reuse what exists, standard library first, minimum that works, one small test for logic with branches/loops/parsers/security.

## Stack
- Backend: FastAPI (Python stdlib + fastapi/uvicorn only)
- Frontend: single static HTML page (no build step, no framework)
- AI: optional generative AI API via env var `GEN_AI_API_KEY`; deterministic fallback when unset

## Commands
- `python -m venv .venv && .venv\Scripts\Activate.ps1`
- `pip install fastapi uvicorn`
- `python -m uvicorn app.main:app --reload`
- `python -m pytest` (tests)
