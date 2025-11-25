import pytest
from flask import Flask
from app import index  # your blueprint
from icalendar import Calendar, Event, Alarm
from datetime import datetime, timezone
import io


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "testkey"
    app.register_blueprint(index)
    return app


def test_get_form(client):
    """GET / should return the form page."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"<form" in response.data


def test_post_invalid_ics(client):
    """POST invalid ICS → should show error message."""
    data = {
        "hours": 1,
        "minutes": 5,
        "submit": True,
        "icsfile": (io.BytesIO(b"not-an-ics"), "invalid.ics")
    }

    response = client.post("/", data=data, content_type="multipart/form-data")

    assert response.status_code == 200
    assert b"can&#39;t read file<" in response.data


def make_simple_ics(with_alarm=False):
    """Create a minimal ICS file as bytes."""
    cal = Calendar()
    event = Event()
    event.add("SUMMARY", "Test Event")
    event.add("DTSTART", datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc))

    if with_alarm:
        alarm = Alarm()
        alarm.add("ACTION", "DISPLAY")
        alarm.add("DESCRIPTION", "Test Event")
        alarm.add("TRIGGER;VALUE=DURATION", "-PT1H0M")
        event.add_component(alarm)

    cal.add_component(event)
    return cal.to_ical()


def test_post_valid_ics_adds_alarm(client):
    """POST valid ICS (no alarm) → should get back a file with one VALARM."""
    ics = make_simple_ics(with_alarm=False)

    data = {
        "hours": 1,
        "minutes": 15,
        "icsfile": (io.BytesIO(ics), "test.ics")
    }

    response = client.post("/", data=data, content_type="multipart/form-data")
    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("text/calendar")
    assert "attachment" in response.headers.get("Content-Disposition", "")

    # Parse returned ICS content
    returned_ics = response.data
    cal = Calendar.from_ical(returned_ics)

    alarms = [
        c for c in cal.walk()
        if c.name == "VALARM"
    ]

    assert len(alarms) == 1
    assert alarms[0].get("TRIGGER").to_ical() == b"-PT1H15M"


@pytest.mark.skip(reason="Not implemented yet")
def test_post_valid_ics_with_existing_alarm(client):
    """ICS already has an alarm → should not add a duplicate."""
    ics = make_simple_ics(with_alarm=True)

    data = {
        "hours": 2,
        "minutes": 30,
        "icsfile": (io.BytesIO(ics), "hasalarm.ics")
    }

    response = client.post("/", data=data, content_type="multipart/form-data")
    assert response.status_code == 200

    returned_ics = response.data
    cal = Calendar.from_ical(returned_ics)

    alarms = [
        c for c in cal.walk()
        if c.name == "VALARM"
    ]

    # Should still be exactly 1
    assert len(alarms) == 1
