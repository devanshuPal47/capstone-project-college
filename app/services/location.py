"""Location / map services using OpenStreetMap Nominatim (free, no API key required)."""
from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


NOMINATIM_BASE = "https://nominatim.openstreetmap.org/search"


def geocode(destination: str) -> dict[str, Any] | None:
    """Look up lat/lon for a destination using OpenStreetMap Nominatim."""
    params = urllib.parse.urlencode({"q": destination, "format": "json", "limit": 1})
    url = f"{NOMINATIM_BASE}?{params}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "skillwallet-travel-planner/1.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            results = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.HTTPError, urllib.error.URLError, OSError):
        return None
    except Exception:
        return None

    if not results:
        return None
    r = results[0]
    return {
        "display_name": r.get("display_name"),
        "lat": float(r.get("lat", 0)),
        "lon": float(r.get("lon", 0)),
        "type": r.get("type"),
    }
