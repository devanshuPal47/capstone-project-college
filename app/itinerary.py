"""Itinerary generation logic.

Gemini AI first (with reasoning), then deterministic fallback builder.
Always respects user inputs: destination, dates, budget, group size, travel style, interests.
"""
from __future__ import annotations

import datetime as _dt
import os
from typing import Any

from app.services.gemini import call_gemini as gemini_call_gemini
from app.services.gemini import DEFAULT_MODEL as GEMINI_DEFAULT_MODEL


def _parse_date(value: str) -> _dt.date:
    return _dt.date.fromisoformat(value)


def _pick(options: list[str], index: int) -> str:
    return options[index % len(options)]


def build_fallback_itinerary(
    destination: str,
    budget: float,
    start_date: str,
    end_date: str,
    interests: list[str],
    group_size: int,
    travel_style: str,
) -> dict[str, Any]:
    """Build a structured day-by-day itinerary without AI (deterministic fallback)."""
    start = _parse_date(start_date)
    end = _parse_date(end_date)
    if end < start:
        raise ValueError("end_date must be on or after start_date")

    days = (end - start).days + 1
    daily_budget = round(budget / days, 2)

    # Style-based pacing modifiers
    pace = {"relaxed": 1, "balanced": 2, "packed": 3}.get(travel_style, 2)

    attractions = [
        "Old Town walking tour",
        "City museum",
        "Local market",
        "Scenic lookout point",
        "Historic waterfront",
        "Botanical garden",
        "Cultural heritage site",
        "Neighborhood exploration",
    ]
    dining = [
        "Neighborhood bistro",
        "Street food stall",
        "Family-run trattoria",
        "Riverside cafe",
        "Local grill",
        "Bakery & coffee shop",
        "Traditional eatery",
        "Seafood restaurant",
    ]
    accommodations = [
        "City-center guesthouse",
        "Budget boutique hotel",
        "Hostel private room",
        "Airbnb apartment",
        "Mid-range hotel",
    ]
    transport = [
        "Walk between sites",
        "Public bus / tram",
        "Rideshare",
        "Rental bike",
        "Metro / subway",
    ]

    itinerary_days: list[dict[str, Any]] = []
    remaining = budget
    for i in range(days):
        day_date = start + _dt.timedelta(days=i)
        # Vary activities based on pace and day index
        activity_count = min(pace, 3)
        morning = _pick(attractions, i)
        afternoon = _pick(attractions, i + 2) if activity_count >= 2 else "Free time / leisure"
        evening = _pick(dining, i)
        day = {
            "day": i + 1,
            "date": day_date.isoformat(),
            "morning": morning,
            "afternoon": afternoon,
            "evening": evening,
            "dining": _pick(dining, i + 3),
            "accommodation": _pick(accommodations, i),
            "transportation": _pick(transport, i),
            "estimated_cost": round(daily_budget, 2),
        }
        itinerary_days.append(day)
        remaining = round(remaining - daily_budget, 2)

    return {
        "destination": destination,
        "start_date": start_date,
        "end_date": end_date,
        "days": days,
        "group_size": group_size,
        "travel_style": travel_style,
        "interests": interests,
        "total_budget": budget,
        "remaining_budget": remaining,
        "generated_with_ai": False,
        "itinerary": itinerary_days,
    }


def generate_itinerary(
    destination: str,
    budget: float,
    start_date: str,
    end_date: str,
    interests: list[str],
    group_size: int,
    travel_style: str,
) -> dict[str, Any]:
    """Generate an itinerary: Gemini AI first, then fallback."""
    # Calculate days for the prompt
    start = _parse_date(start_date)
    end = _parse_date(end_date)
    days = (end - start).days + 1

    # Try Gemini AI with reasoning
    if os.getenv("GEMINI_API_KEY"):
        result = gemini_call_gemini(
            model=os.getenv("GEMINI_MODEL", GEMINI_DEFAULT_MODEL),
            destination=destination,
            budget=budget,
            start_date=start_date,
            end_date=end_date,
            interests=interests,
            group_size=group_size,
            travel_style=travel_style,
            days=days,
        )
        if result is not None:
            result.setdefault("destination", destination)
            result.setdefault("start_date", start_date)
            result.setdefault("end_date", end_date)
            result.setdefault("days", days)
            result.setdefault("group_size", group_size)
            result.setdefault("travel_style", travel_style)
            result.setdefault("interests", interests)
            result.setdefault("total_budget", budget)
            result["generated_with_ai"] = True
            return result

    # Fallback to deterministic builder
    return build_fallback_itinerary(
        destination, budget, start_date, end_date, interests, group_size, travel_style
    )
