"""FastAPI backend for the Personalized Travel Itinerary Planner."""
from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.itinerary import generate_itinerary

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
