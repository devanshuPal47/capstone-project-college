# Personalized Travel Itinerary Planner

Very simple MVP of the travel itinerary planner. FastAPI backend + static HTML frontend, with a deterministic itinerary builder (works without any AI key) and optional Generative AI / Supabase enhancements.

## Stack
- Backend: FastAPI (Python stdlib + fastapi/uvicorn only)
- Frontend: single static HTML page (`public/index.html`), no build step
- AI: optional via `GEN_AI_API_KEY` / `GEN_AI_ENDPOINT`; deterministic fallback when unset
- Supabase: optional trip persistence via `SUPABASE_URL` / `SUPABASE_ANON_KEY`; degrades gracefully when unset

## Prerequisites
- Python 3.12+
- (optional) Node only if you later add a React frontend — not required for this MVP

## Install ponytail skill (done)
- `AGENTS.md` — project rules (ponytail ladder: reuse existing, stdlib first, minimum that works, one small test)
- `skills/ponytail/SKILL.md` — the ponytail skill prompt

## Install & run locally
```powershell
# 1. Create venv
python -m venv .venv
.venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install fastapi uvicorn pydantic pytest

# 3. (optional) Configure env
copy .env.example .env
# then edit .env with your GEN_AI_* and SUPABASE_* values

# 4. Run the backend
python -m uvicorn app.main:app --reload
```
Backend: `http://localhost:8000`
Frontend: open `public/index.html` in a browser (it calls `http://localhost:8000/generate-itinerary`)

## Endpoints
- `GET /health` — status
- `POST /generate-itinerary` — body: `{destination, budget, start_date, end_date, interests[], group_size, travel_style}` → day-by-day itinerary
- `GET /destinations` — recommended destination list
- `GET /trips` — saved trips (Supabase only; empty if not configured)
- `GET /trips/{trip_id}` — single trip (Supabase only)

## Run tests
```powershell
.venv\Scripts\Activate.ps1
python -m pytest
```
Currently 3 tests pass (itinerary structure/branches, end-before-start error, Supabase graceful degradation).

## Epic coverage (code-implementable)
| Epic / Activity | Status |
|---|---|
| Epic 1: Environment setup | venv + requirements.txt done |
| Epic 2.1: Create Supabase project | external — you create in Supabase dashboard |
| Epic 2.2: Create tables | external — create `trips` table in Supabase SQL editor |
| Epic 2.3: Store API keys in .env | `.env.example` done; fill `.env` |
| Epic 3.1: User Preference Capture | `ItineraryRequest` model done |
| Epic 3.2: Prompt Structuring Logic | `build_fallback_itinerary` done |
| Epic 3.3: Destination Recommendation | `GET /destinations` done |
| Epic 4.1: Daily Itinerary Builder | done |
| Epic 4.2: Route & Time Optimization | sequential day builder done |
| Epic 4.3: Vibe-Based Personalization | `travel_style` param done |
| Epic 5.1: Trip Save & Management | `save_trip` + `/trips` endpoints done |
| Epic 5.2: Share & Export | frontend prints/saves; `/trips/{id}` retrieve done |
| Epic 5.3/5.4: Testing & Env config | tests + `.env.example` done |
| Epic 6.1: Deploy Backend to Render | external — deploy this repo to Render |
| Epic 6.2: Deploy Frontend to Vercel | external — point Vercel at `public/` or serve via backend |
| Epic 7.1: Functional Testing | tests done |
| Epic 7.2: Validate Database Updates | run `GET /trips` after configuring Supabase |

## Items you must complete externally (not code I can create)
- **Install Cursor IDE & set up GitHub repo** (Epic 1.1)
- **Create Supabase project + `trips` table** (Epic 2.1, 2.2) — columns: `id`, `created_at`, plus the itinerary response fields
- **Deploy backend to Render** (Epic 6.1)
- **Deploy frontend to Vercel** (Epic 6.2)
- **JWT / AI Token / Credits system** — not included in this simple MVP; add auth later if needed

## What was skipped / not checked
- No JWT/auth, AI token, or credits system (kept minimal per "very simple version" request)
- No React frontend (single HTML page used instead)
- Supabase table must be created manually; saving degrades gracefully if absent
- AI integration only works if `GEN_AI_API_KEY` + `GEN_AI_ENDPOINT` are set and reachable
