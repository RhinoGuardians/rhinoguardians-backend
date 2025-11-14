"""Test the API endpoints"""
from datetime import datetime
import pytest
from fastapi.testclient import TestClient

def test_read_root(client: TestClient):
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to RhinoGuardians API"}

def test_health_check(client: TestClient):
    """Test the health check endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_get_alerts_empty(client: TestClient):
    """Test getting alerts when none exist"""
    response = client.get("/alerts/")
    assert response.status_code == 200
    assert response.json() == {"alerts": []}