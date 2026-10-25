"""Itinerary generation logic.

Gemini AI first (with reasoning), then deterministic fallback builder.
Always respects user inputs: destination, dates, budget, group size, travel style, interests.
"""
from __future__ import annotations

import datetime as _dt
import os
from dotenv import load_dotenv
from typing import Any

load_dotenv()

from app.services.gemini import call_gemini as gemini_call_gemini
from app.services.gemini import DEFAULT_MODEL as GEMINI_DEFAULT_MODEL
from app.services.location import geocode


def _parse_date(value: str) -> _dt.date:
    return _dt.date.fromisoformat(value)


def _pick(options: list[str], index: int) -> str:
    return options[index % len(options)]


def _destination_keywords(destination: str) -> str:
    """Normalize destination for keyword matching."""
    return destination.lower()


def _is_india(dest: str) -> bool:
    return any(k in dest for k in ["india", "indore", "mumbai", "delhi", "bangalore", "goa", "jaipur"])


def _is_europe(dest: str) -> bool:
    return any(k in dest for k in ["paris", "rome", "london", "barcelona", "prague", "amsterdam", "berlin"])


def _is_asia(dest: str) -> bool:
    return any(k in dest for k in ["tokyo", "bangkok", "bali", "singapore", "seoul", "hong kong", "kyoto"])


def _is_usa(dest: str) -> bool:
    return any(k in dest for k in ["new york", "los angeles", "chicago", "san francisco", "miami", "las vegas"])


def _attractions_for(destination: str, interests: list[str], travel_style: str) -> list[str]:
    """Build destination- and interest-specific attraction list."""
    d = _destination_keywords(destination)
    interests_joined = ",".join(i.lower() for i in interests)

    # Base attractions by region
    if _is_india(d):
        base = [
            f"Historic sites in {destination}",
            f"Local bazaar and market in {destination}",
            f"Heritage walking tour of {destination}",
            f"City palace or fort in {destination}",
            f"Local temple visit in {destination}",
            f"Street art walk in {destination}",
            f"City museum in {destination}",
            f"Scenic viewpoint in {destination}",
        ]
    elif _is_europe(d):
        base = [
            f"Old Town walking tour of {destination}",
            f"City museum in {destination}",
            f"Historic cathedral in {destination}",
            f"Scenic riverfront in {destination}",
            f"Castle or palace in {destination}",
            f"Local art gallery in {destination}",
            f"Cobblestone street stroll in {destination}",
            f"City park in {destination}",
        ]
    elif _is_asia(d):
        base = [
            f"Temple or shrine in {destination}",
            f"Night market in {destination}",
            f"City skyline viewpoint in {destination}",
            f"Local market street in {destination}",
            f"Historic palace in {destination}",
            f"Botanical garden in {destination}",
            f"Riverside walk in {destination}",
            f"Cultural center in {destination}",
        ]
    elif _is_usa(d):
        base = [
            f"Downtown walking tour of {destination}",
            f"City museum in {destination}",
            f"Central park in {destination}",
            f"Historic landmark in {destination}",
            f"Local food hall in {destination}",
            f"Art gallery district in {destination}",
            f"Waterfront promenade in {destination}",
            f"Observation deck in {destination}",
        ]
    else:
        base = [
            f"Old Town walking tour of {destination}",
            f"City museum in {destination}",
            f"Local market in {destination}",
            f"Scenic lookout point in {destination}",
            f"Historic waterfront in {destination}",
            f"Botanical garden in {destination}",
            f"Cultural heritage site in {destination}",
            f"Neighborhood exploration in {destination}",
        ]

    # Interest-based additions
    interest_extras: list[str] = []
    for interest in interests:
        low = interest.lower()
        if any(k in low for k in ["food", "dining", "culinary"]):
            interest_extras.extend([
                f"Food market tour in {destination}",
                f"Local cooking class in {destination}",
                f"Street food crawl in {destination}",
            ])
        if any(k in low for k in ["culture", "history", "heritage"]):
            interest_extras.extend([
                f"Heritage museum in {destination}",
                f"Historic district tour in {destination}",
                f"Local cultural center in {destination}",
            ])
        if any(k in low for k in ["nature", "outdoors"]):
            interest_extras.extend([
                f"Nature park in {destination}",
                f"Scenic hiking trail near {destination}",
                f"Botanical garden in {destination}",
            ])
        if any(k in low for k in ["art", "museum"]):
            interest_extras.extend([
                f"Art museum in {destination}",
                f"Local gallery walk in {destination}",
                f"Street art tour in {destination}",
            ])
        if any(k in low for k in ["shopping"]):
            interest_extras.extend([
                f"Local shopping district in {destination}",
                f"Craft market in {destination}",
                f"Boutique street in {destination}",
            ])
        if any(k in low for k in ["nightlife", "bar", "pub"]):
            interest_extras.extend([
                f"Local pub crawl in {destination}",
                f"Rooftop bar in {destination}",
                f"Live music venue in {destination}",
            ])
        if any(k in low for k in ["wellness", "spa"]):
            interest_extras.extend([
                f"Local spa in {destination}",
                f"Wellness center in {destination}",
                f"Yoga studio in {destination}",
            ])
        if any(k in low for k in ["adventure", "sports"]):
            interest_extras.extend([
                f"Adventure activity in {destination}",
                f"Outdoor sports near {destination}",
                f"Adventure park in {destination}",
            ])

    # Pace-based filtering
    pace_limit = {"relaxed": 6, "balanced": 10, "packed": 14}.get(travel_style, 10)
    combined = base + interest_extras
    return combined[:pace_limit]


def _dining_for(destination: str, interests: list[str]) -> list[str]:
    """Build destination- and interest-specific dining list."""
    d = _destination_keywords(destination)
    interests_joined = ",".join(i.lower() for i in interests)

    if _is_india(d):
        base = [
            f"Local thali restaurant in {destination}",
            f"Street food stall in {destination}",
            f"Traditional dhaba in {destination}",
            f"Rooftop cafe in {destination}",
            f"Chai and snacks stall in {destination}",
            f"Regional cuisine restaurant in {destination}",
            f"Sweet shop in {destination}",
            f"Lassi corner in {destination}",
        ]
    elif _is_europe(d):
        base = [
            f"Neighborhood bistro in {destination}",
            f"Local cafe in {destination}",
            f"Traditional trattoria in {destination}",
            f"Wine bar in {destination}",
            f"Bakery in {destination}",
            f"Local grill in {destination}",
            f"Cheese shop in {destination}",
            f"Patisserie in {destination}",
        ]
    else:
        base = [
            f"Neighborhood bistro in {destination}",
            f"Street food stall in {destination}",
            f"Family-run restaurant in {destination}",
            f"Riverside cafe in {destination}",
            f"Local grill in {destination}",
            f"Bakery & coffee shop in {destination}",
            f"Traditional eatery in {destination}",
            f"Seafood restaurant in {destination}",
        ]

    interest_extras: list[str] = []
    for interest in interests:
        low = interest.lower()
        if any(k in low for k in ["food", "dining", "culinary"]):
            interest_extras.extend([
                f"Food tour in {destination}",
                f"Local cooking class in {destination}",
                f"Street food crawl in {destination}",
            ])

    return base + interest_extras


def _accommodations_for(destination: str, group_size: int, budget: float) -> list[str]:
    """Build destination-specific accommodation list."""
    d = _destination_keywords(destination)
    per_person = budget / max(group_size, 1)

    if per_person < 50:
        tier = ["Hostel dorm", "Budget guesthouse", "Backpacker hostel"]
    elif per_person < 150:
        tier = ["Budget boutique hotel", "City-center guesthouse", "Airbnb apartment"]
    else:
        tier = ["Mid-range hotel", "Boutique hotel", "Heritage property"]

    return [f"{t} in {destination}" for t in tier]


def _transport_for(destination: str) -> list[str]:
    """Build destination-specific transport list."""
    d = _destination_keywords(destination)
    if _is_india(d):
        return ["Auto-rickshaw", "Local bus", "Metro", "Rideshare (Uber/Ola)", "Walking between sites"]
    return ["Walk between sites", "Public bus / tram", "Rideshare", "Rental bike", "Metro / subway"]


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

    # Style-based pacing
    pace = {"relaxed": 1, "balanced": 2, "packed": 3}.get(travel_style, 2)

    # Destination-specific content
    attractions = _attractions_for(destination, interests, travel_style)
    dining = _dining_for(destination, interests)
    accommodations = _accommodations_for(destination, group_size, budget)
    transport = _transport_for(destination)

    # Get location coordinates
    location = geocode(destination)
    lat = location["lat"] if location else None
    lon = location["lon"] if location else None

    itinerary_days: list[dict[str, Any]] = []
    remaining = budget
    for i in range(days):
        day_date = start + _dt.timedelta(days=i)
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
        "location": {"lat": lat, "lon": lon} if lat and lon else None,
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

    # Get location coordinates for map display
    location = geocode(destination)

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
            result["location"] = (
                {"lat": location["lat"], "lon": location["lon"]}
                if location and location.get("lat") and location.get("lon")
                else None
            )
            return result

    # Fallback to deterministic builder
    return build_fallback_itinerary(
        destination, budget, start_date, end_date, interests, group_size, travel_style
    )
