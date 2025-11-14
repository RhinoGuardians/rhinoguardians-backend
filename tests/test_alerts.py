import json

AUTH = {"Authorization": "Bearer testtoken123"}

def test_alerts_list_empty(client):
    resp = client.get("/alerts/")
    assert resp.status_code == 200
    data = resp.json()
    assert "alerts" in data
    assert isinstance(data["alerts"], list)
    assert data["total"] == 0

def test_alerts_trigger_requires_auth(client):
    payload = {
        "detection_id": "det_unauth",
        "type": "poacher_suspected",
        "severity": "critical",
        "source": "camera_trap",
        "location": {"lat": -1.0, "lng": 36.0, "zoneLabel": "Test Zone"},
        "createdBy": "Tester",
    }
    resp = client.post("/alerts/trigger", json=payload)
    assert resp.status_code == 401

def test_alerts_trigger_success_and_list(client):
    payload = {
        "detection_id": "det_123",
        "type": "poacher_suspected",
        "severity": "critical",
        "source": "camera_trap",
        "notes": "2 individuals on foot",
        "location": {"lat": -23.8859, "lng": 31.5205, "zoneLabel": "North Sector"},
        "createdBy": "Operator 1",
    }
    # Create alert
    resp = client.post("/alerts/trigger", headers=AUTH, json=payload)
    assert resp.status_code == 200
    body = resp.json()
    # Response model fields
    assert body["detection_id"] == "det_123"
    assert body["type"] == "poacher_suspected"
    assert body["severity"] == "critical"
    assert body["status"] in ("sent", "failed", "created", "acknowledged", "in_progress", "resolved", "expired")
    assert "created_at" in body and "updated_at" in body
    assert body["location"]["zoneLabel"] == "North Sector"

    # List alerts should show 1+
    list_resp = client.get("/alerts/")
    assert list_resp.status_code == 200
    lst = list_resp.json()
    assert lst["total"] >= 1
    assert any(a["detection_id"] == "det_123" for a in lst["alerts"])

def test_alerts_update_status(client):
    # Create alert
    payload = {
        "detection_id": "det_to_update",
        "type": "vehicle_suspected",
        "severity": "high",
        "source": "camera_trap",
        "location": {"lat": 0.0, "lng": 0.0, "zoneLabel": "Z1"},
        "createdBy": "Updater",
    }
    resp = client.post("/alerts/trigger", headers=AUTH, json=payload)
    assert resp.status_code == 200

    # Find its DB id from listing
    lst = client.get("/alerts/").json()
    assert lst["alerts"], "expected at least one alert in list"
    # last created should be first due to order by timestamp desc
    alert_id = lst["alerts"][0]["id"]

    # Update status to ACKNOWLEDGED (DB enum)
    upd = client.patch(f"/alerts/{alert_id}/status", params={"new_status": "ACKNOWLEDGED"})
    assert upd.status_code == 200
    updated = upd.json()
    assert updated["id"] == alert_id
    assert updated["status"] in ("ACKNOWLEDGED", "INACTIVE", "ACTIVE", "RESOLVED")