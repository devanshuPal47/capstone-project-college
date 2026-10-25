"""FastAPI backend for the Personalized Travel Itinerary Planner."""
from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.itinerary import generate_itinerary
from app.supabase import save_trip, list_trips, get_trip

app = FastAPI(title="Personalized Travel Itinerary Planner")


class ItineraryRequest(BaseModel):
    destination: str = Field(..., min_length=1)
    budget: float = Field(..., gt=0)
    start_date: str
    end_date: str
    interests: list[str] = Field(default_factory=list)
    group_size: int = Field(default=1, gt=0)
    travel_style: str = Field(default="balanced")


class ItineraryResponse(BaseModel):
    destination: str
    start_date: str
    end_date: str
    days: int
    group_size: int
    travel_style: str
    interests: list[str]
    total_budget: float
    remaining_budget: float
    generated_with_ai: bool
    itinerary: list[dict]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/destinations")
def destinations() -> dict[str, list[str]]:
    """Simple destination recommendation engine (no AI key required)."""
    return {
        "destinations": [
            "Paris", "Tokyo", "New York", "Bali", "Rome",
            "Barcelona", "Kyoto", "London", "Bangkok", "Sydney",
        ]
    }


@app.get("/trips")
def trips() -> list[dict]:
    """List saved trips from Supabase (empty if Supabase not configured)."""
    return list_trips()


@app.get("/trips/{trip_id}")
def trip(trip_id: str) -> dict | None:
    """Retrieve a single saved trip from Supabase."""
    return get_trip(trip_id)


@app.post("/generate-itinerary", response_model=ItineraryResponse)
def generate(request: ItineraryRequest) -> ItineraryResponse:
    try:
        result = generate_itinerary(
            destination=request.destination,
            budget=request.budget,
            start_date=request.start_date,
            end_date=request.end_date,
            interests=request.interests,
            group_size=request.group_size,
            travel_style=request.travel_style,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    # Best-effort persistence: degrade gracefully when Supabase is not configured.
    try:
        save_trip(result)
    except Exception:  # noqa: BLE001 - never let storage failure block the user
        pass

    return ItineraryResponse(**result)
