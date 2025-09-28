from fastapi.testclient import TestClient
from app.main import app


def run() -> None:
    c = TestClient(app)
    print("health", c.get("/health").json())
    u = c.post("/users/", json={"name": "Test", "email": "test@example.com", "timezone": "UTC"})
    print("user_status", u.status_code)
    uid = u.json()["id"]
    m = c.post(
        "/mood-logs/",
        json={"user_id": uid, "mood_score": 7, "mood_tags": "calm", "note_text": "Feeling okay"},
    )
    print("mood_status", m.status_code)
    print("trend", c.get(f"/analytics/mood-trend/{uid}").json())
    print("sentiment", c.post("/analytics/sentiment", params={"text": "I feel great"}).json())


if __name__ == "__main__":
    run()

