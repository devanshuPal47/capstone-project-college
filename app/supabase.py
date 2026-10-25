"""Minimal Supabase REST client using the standard library only.

Reads ``SUPABASE_URL`` and ``SUPABASE_ANON_KEY`` from the environment.
Degrades gracefully when credentials are absent so the app keeps working
without Supabase configured.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any


def _headers() -> dict[str, str] | None:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")
    if not url or not key:
        return None
    return {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }


def _request(method: str, path: str, payload: dict[str, Any] | None = None) -> Any:
    headers = _headers()
    if headers is None:
        return None
    url = os.getenv("SUPABASE_URL", "").rstrip("/") + path
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8")
        raise RuntimeError(f"Supabase {method} {path} failed ({exc.code}): {body}")
    return json.loads(body) if body else None


def save_trip(trip: dict[str, Any]) -> dict[str, Any] | None:
    """Persist a generated itinerary to Supabase. Returns the inserted row."""
    result = _request("POST", "/rest/v1/trips", payload=trip)
    if isinstance(result, list) and result:
        return result[0]
    return result


def list_trips(limit: int = 50) -> list[dict[str, Any]]:
    """Fetch recent trips from Supabase."""
    path = f"/rest/v1/trips?select=*&order=created_at.desc&limit={limit}"
    result = _request("GET", path)
    return result if isinstance(result, list) else []


def get_trip(trip_id: str) -> dict[str, Any] | None:
    """Fetch a single trip by id from Supabase."""
    path = f"/rest/v1/trips?id=eq.{trip_id}&select=*"
    result = _request("GET", path)
    if isinstance(result, list) and result:
        return result[0]
    return None
