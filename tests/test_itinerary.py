from __future__ import annotations

import pytest

from app.itinerary import build_fallback_itinerary


def test_fallback_itinerary_structure_and_branches():
    result = build_fallback_itinerary(
        destination="Paris",
        budget=900.0,
        start_date="2026-11-01",
        end_date="2026-11-03",
        interests=["food", "sightseeing"],
        group_size=2,
        travel_style="relaxed",
    )

    assert result["destination"] == "Paris"
    assert result["days"] == 3
    assert result["group_size"] == 2
    assert result["generated_with_ai"] is False
    assert len(result["itinerary"]) == 3

    # Each day has the required fields and stays within per-day budget.
    daily = result["total_budget"] / result["days"]
    for day in result["itinerary"]:
        assert set(day) >= {
            "day", "date", "morning", "afternoon", "evening",
            "dining", "accommodation", "transportation", "estimated_cost",
        }
        assert day["estimated_cost"] <= daily + 0.01

    # Total estimated cost does not exceed the budget.
    total = sum(d["estimated_cost"] for d in result["itinerary"])
    assert round(total, 2) <= result["total_budget"] + 0.01


def test_end_date_before_start_date_raises():
    with pytest.raises(ValueError):
        build_fallback_itinerary(
            destination="Paris",
            budget=900.0,
            start_date="2026-11-03",
            end_date="2026-11-01",
            interests=[],
            group_size=1,
            travel_style="balanced",
        )
