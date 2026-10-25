# Skillwallet Travel — Personalized Itinerary Planner

A beautiful, soothing, AI-powered travel itinerary planner with a React + Tailwind frontend and FastAPI backend.

## 🎨 UI/UX

- **Soothing color palette** — sage greens, soft indigos, warm neutrals
- **Glassmorphism** — backdrop-blur panels with subtle borders
- **Responsive design** — works on mobile, tablet, and desktop
- **Smooth animations** — fade-in, slide-up transitions
- **Dark mode toggle** — light/dark theme support
- **Trip cards** — clean, scannable day-by-day layouts

## 📁 Project Structure

```
college/
├── app/                    # FastAPI backend
│   ├── main.py             # API routes & CORS
│   ├── itinerary.py        # Itinerary generation (Groq + fallback)
│   ├── services/
│   │   ├── groq.py         # Groq AI client with reasoning
│   │   └── location.py     # OpenStreetMap geocoding
│   └── tests/              # Backend tests
├── client/                 # React + Vite + Tailwind frontend
│   ├── src/
│   │   ├── components/     # Navbar, TripBuilder, ItineraryView
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── utils/          # Helpers, constants, API service
│   │   ├── services/       # API client
│   │   └── assets/
│   ├── dist/               # Built frontend
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js
├── .env                    # Your API keys (create from .env.example)
├── .env.example
├── requirements.txt
└── README.md
```

## 🚀 Quick Start

### 1. Backend

```powershell
# Create & activate venv
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install dependencies
pip install fastapi uvicorn pydantic pytest psycopg2-binary

# Copy env template and add your keys
copy .env.example .env
# Edit .env with your GROQ_API_KEY

# Start server (port 8001 since 8000 may be blocked)
python -m uvicorn app.main:app --reload --port 8001
```

Backend: `http://127.0.0.1:8001`  
API docs: `http://127.0.0.1:8001/docs`

### 2. Frontend (Development)

```powershell
cd client
npm install
npm run dev
```

Frontend: `http://localhost:5173` (proxies `/api` to backend on 8001)

### 3. Frontend (Production Build)

```powershell
cd client
npm run build
# Serves static files from client/dist/
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/destinations` | Popular destination list |
| `POST` | `/generate-itinerary` | Generate AI itinerary |
| `POST` | `/location` | Geocode destination (lat/lon) |
| `GET` | `/trips` | List saved trips |
| `GET` | `/trips/{id}` | Get single trip |

### Generate Itinerary Request

```json
{
  "destination": "Paris, France",
  "budget": 900,
  "start_date": "2026-11-01",
  "end_date": "2026-11-03",
  "interests": ["food", "sightseeing", "culture"],
  "group_size": 2,
  "travel_style": "relaxed"
}
```

## 🤖 AI Integration

The planner uses **Groq** (`openai/gpt-oss-120b`) with structured reasoning:

1. **System prompt** enforces strict adherence to user inputs (budget, dates, style, interests)
2. **JSON mode** ensures valid, parseable output
3. **Graceful fallback** — deterministic template builder if Groq is unavailable

To enable AI: set `GROQ_API_KEY` in `.env`. Get a free key at [console.groq.com](https://console.groq.com/).

## 🗺️ Location / Map

Uses **OpenStreetMap Nominatim** (free, no API key) for geocoding destinations to lat/lon coordinates via the `/location` endpoint.

## 🧪 Tests

```powershell
.venv\Scripts\Activate.ps1
python -m pytest
```

Currently 6 tests pass (itinerary structure, branches, error handling, Groq degradation).

## 📝 Notes

- Port 8000 may be blocked on some systems — use `--port 8001`
- `.env` is gitignored — never commit your API keys
- The Groq key must be valid for AI generation; otherwise the smart template builder is used
