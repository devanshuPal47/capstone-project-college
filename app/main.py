"""FastAPI backend for the Personalized Travel Itinerary Planner."""
from __future__ import annotations

import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.itinerary import generate_itinerary
from app.services.location import geocode

app = FastAPI(title="Skillwallet Travel — Personalized Itinerary Planner")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ItineraryRequest(BaseModel):
    destination: str = Field(..., min_length=1, description="Travel destination")
    budget: float = Field(..., gt=0, description="Total budget in USD")
    start_date: str = Field(..., description="Start date (YYYY-MM-DD)")
    end_date: str = Field(..., description="End date (YYYY-MM-DD)")
    interests: list[str] = Field(default_factory=list, description="User interests")
    group_size: int = Field(default=1, gt=0, description="Number of travelers")
    travel_style: str = Field(default="balanced", description="relaxed | balanced | packed")


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
    location: dict | None = None
    itinerary: list[dict]


class LocationRequest(BaseModel):
    destination: str


class LocationResponse(BaseModel):
    display_name: str
    lat: float
    lon: float
    type: str | None = None


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/destinations")
def destinations() -> dict[str, list[str]]:
    """Popular destination recommendations."""
    return {
        "destinations": [
            "Paris, France",
            "Tokyo, Japan",
            "New York, USA",
            "Bali, Indonesia",
            "Rome, Italy",
            "Barcelona, Spain",
            "Kyoto, Japan",
            "London, UK",
            "Bangkok, Thailand",
            "Sydney, Australia",
            "Santorini, Greece",
            "Cape Town, South Africa",
            "Reykjavik, Iceland",
            "Marrakech, Morocco",
            "Vancouver, Canada",
        ]
    }


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
    return ItineraryResponse(**result)


@app.post("/location", response_model=LocationResponse)
def get_location(req: LocationRequest) -> LocationResponse:
    """Geocode a destination using OpenStreetMap Nominatim (free map API)."""
    loc = geocode(req.destination)
    if loc is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return LocationResponse(**loc)


@app.get("/trips")
def trips() -> list[dict]:
    """List saved trips (placeholder for Supabase integration)."""
    return []


@app.get("/trips/{trip_id}")
def trip(trip_id: str) -> dict | None:
    """Retrieve a single saved trip (placeholder for Supabase integration)."""
    return None
