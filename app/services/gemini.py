"""Google Gemini generative AI client using the standard library only.

Uses Gemini's REST API:
POST https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}

Reads GEMINI_API_KEY and GEMINI_MODEL from the environment. Degrades gracefully
when the key is absent.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

DEFAULT_MODEL = "gemini-2.5-flash"  # Confirmed working on v1beta
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


def _headers() -> dict[str, str] | None:
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        return None
    return {"Content-Type": "application/json"}


def build_system_prompt() -> str:
    return (
        "You are an expert travel itinerary planner. "
        "Create detailed, day-by-day travel itineraries that strictly follow the user's inputs. "
        "Rules: "
        "1) Every suggestion must match the destination, dates, budget, group size, travel style, and interests provided. "
        "2) Stay within the total budget - estimated daily costs must not exceed budget / number of days. "
        "3) Match the travel style: relaxed = slower pace with free time, balanced = moderate, packed = back-to-back activities. "
        "4) Match the interests - only include activities, dining, and attractions relevant to the stated interests. "
        "5) Group size affects accommodation and transportation recommendations. "
        "6) Output valid JSON only, no markdown fences, no extra text. "
        "7) Each day needs: day, date, morning, afternoon, evening, dining, accommodation, transportation, estimated_cost. "
        "8) Be specific and realistic - mention actual types of places, not generic descriptions. "
        "9) Consider travel time between activities - don't schedule things far apart back-to-back."
    )


def build_user_prompt(
    destination: str,
    budget: float,
    start_date: str,
    end_date: str,
    interests: list[str],
    group_size: int,
    travel_style: str,
    days: int,
) -> str:
    interests_str = ", ".join(interests) if interests else "general exploration"
    daily_budget = round(budget / days, 2)
    return (
        f"Create a {days}-day travel itinerary for {destination} from {start_date} to {end_date}. "
        f"Total budget: ${budget:,.2f} (daily budget: ${daily_budget:,.2f}). "
        f"Group size: {group_size} traveler(s). Travel style: {travel_style}. "
        f"Interests: {interests_str}. "
        f"Return a JSON object with keys: destination, start_date, end_date, days, group_size, "
        f"travel_style, interests, total_budget, remaining_budget, generated_with_ai (true), "
        f"and itinerary (array of {days} day objects). "
        f"Each day object needs: day (number), date (YYYY-MM-DD), morning, afternoon, evening, dining, "
        f"accommodation, transportation, estimated_cost (number, within daily budget). "
        f"Be specific about location types that match the interests. Valid JSON only."
    )


def call_gemini(
    model: str,
    destination: str,
    budget: float,
    start_date: str,
    end_date: str,
    interests: list[str],
    group_size: int,
    travel_style: str,
    days: int,
) -> dict[str, Any] | None:
    """Call Gemini generateContent and return parsed itinerary JSON, or None on failure."""
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        return None

    url = BASE_URL.format(model=model or DEFAULT_MODEL) + f"?key={key}"

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"{build_system_prompt()}\n\n{build_user_prompt(
                            destination, budget, start_date, end_date, interests, group_size, travel_style, days
                        )}"
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.4,
            "responseMimeType": "application/json",
        },
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=_headers(), method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = resp.read().decode("utf-8")
    except (urllib.error.HTTPError, urllib.error.URLError, OSError):
        return None
    except Exception:
        return None

    try:
        result = json.loads(body)
        # Gemini response structure: candidates[0].content.parts[0].text
        candidates = result.get("candidates", [])
        if not candidates:
            return None
        parts = candidates[0].get("content", {}).get("parts", [])
        if not parts:
            return None
        text = parts[0].get("text", "")
        itinerary = json.loads(text)
        itinerary["generated_with_ai"] = True
        if "itinerary" not in itinerary or not isinstance(itinerary["itinerary"], list):
            return None
        return itinerary
    except (KeyError, IndexError, json.JSONDecodeError, TypeError):
        return None
