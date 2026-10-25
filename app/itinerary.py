"""Itinerary generation logic.

Deterministic fallback builder used when no GEN_AI_API_KEY is configured.
Optionally enhanced by a generative AI API when the key is present.
"""
from __future__ import annotations

import datetime as _dt
import json
import os
import urllib.error
import urllib.request
from typing import Any


def _parse_date(value: str) -> _dt.date:
    return _dt.date.fromisoformat(value)


def _currency(value: float) -> str:
    return f"${value:,.2f}"


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
    """Build a structured day-by-day itinerary without calling any AI API."""
    start = _parse_date(start_date)
    end = _parse_date(end_date)
    if end < start:
        raise ValueError("end_date must be on or after start_date")

    days = (end - start).days + 1
    daily_budget = round(budget / days, 2)

    attractions = [
        "Old Town walking tour",
        "City museum",
        "Local market",
        "Scenic lookout point",
        "Historic waterfront",
        "Botanical garden",
    ]
    dining = [
        "Neighborhood bistro",
        "Street food stall",
        "Family-run trattoria",
        "Riverside cafe",
        "Local grill",
        "Bakery & coffee shop",
    ]
    accommodations = [
        "City-center guesthouse",
        "Budget boutique hotel",
        "Hostel private room",
        "Airbnb apartment",
    ]
    transport = [
        "Walk between sites",
        "Public bus / tram",
        "Rideshare",
        "Rental bike",
    ]

    itinerary_days: list[dict[str, Any]] = []
    remaining = budget
    for i in range(days):
        day_date = start + _dt.timedelta(days=i)
        day = {
            "day": i + 1,
            "date": day_date.isoformat(),
            "morning": _pick(attractions, i),
            "afternoon": _pick(attractions, i + 2),
            "evening": _pick(dining, i),
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
    """Generate an itinerary, using AI when available, else the fallback."""
    api_key = os.getenv("GEN_AI_API_KEY")
    endpoint = os.getenv("GEN_AI_ENDPOINT")
    if api_key and endpoint:
        try:
            return _call_ai_api(
                endpoint,
                api_key,
                destination,
                budget,
                start_date,
                end_date,
                interests,
                group_size,
                travel_style,
            )
        except Exception:  # noqa: BLE001 - degrade gracefully to fallback
            pass
    return build_fallback_itinerary(
        destination, budget, start_date, end_date, interests, group_size, travel_style
    )


def _call_ai_api(
    endpoint: str,
    api_key: str,
    destination: str,
    budget: float,
    start_date: str,
    end_date: str,
    interests: list[str],
    group_size: int,
    travel_style: str,
) -> dict[str, Any]:
    payload = {
        "destination": destination,
        "budget": budget,
        "start_date": start_date,
        "end_date": end_date,
        "interests": interests,
        "group_size": group_size,
        "travel_style": travel_style,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read().decode("utf-8")
    result = json.loads(body)
    result["generated_with_ai"] = True
    return result
