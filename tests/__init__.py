from app.main import app


def test_health():
    client = app.test_client() if hasattr(app, "test_client") else None
    # FastAPI TestClient preferred; keep this a smoke import guard.
    assert app.title == "Personalized Travel Itinerary Planner"
