from __future__ import annotations

import os

import pytest

import app.services.gemini as gemini


def test_build_prompt_contains_all_fields():
    prompt = gemini.build_user_prompt(
        destination="Paris",
        budget=900.0,
        start_date="2026-11-01",
        end_date="2026-11-03",
        interests=["food", "sightseeing"],
        group_size=2,
        travel_style="relaxed",
        days=3,
    )
    assert isinstance(prompt, str)
    for field in ["Paris", "900", "2026-11-01", "2026-11-03", "food", "sightseeing", "2", "relaxed", "JSON"]:
        assert field in prompt


def test_call_gemini_degrades_without_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    result = gemini.call_gemini(
        gemini.DEFAULT_MODEL, "Paris", 900.0, "2026-11-01", "2026-11-03",
        ["food"], 2, "relaxed", 3,
    )
    assert result is None


def test_default_model():
    assert gemini.DEFAULT_MODEL == "gemini-2.5-flash"
