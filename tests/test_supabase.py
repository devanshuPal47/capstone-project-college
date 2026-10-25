from __future__ import annotations

import os

import pytest

import app.supabase as supabase


def test_supabase_degrades_gracefully_without_credentials(monkeypatch):
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_ANON_KEY", raising=False)
    assert supabase._headers() is None
    assert supabase.save_trip({"x": 1}) is None
    assert supabase.list_trips() == []
