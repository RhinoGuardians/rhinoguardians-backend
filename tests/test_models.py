"""Test the database models and operations"""
import pytest
from datetime import datetime, UTC
from sqlalchemy.orm import Session
from database.models import Detection

def test_create_detection(test_db: Session):
    """Test creating a new detection"""
    detection = Detection(
        timestamp=datetime.now(UTC),
        class_name="rhino",
        confidence=0.95,
        image_path="/path/to/image.jpg",
        gps_lat=-23.8859,
        gps_lng=31.5205
    )
    test_db.add(detection)
    test_db.commit()
    test_db.refresh(detection)

    assert detection.id is not None
    assert detection.class_name == "rhino"
    assert detection.confidence == 0.95
    assert detection.image_path == "/path/to/image.jpg"
    assert detection.gps_lat == -23.8859
    assert detection.gps_lng == 31.5205

def test_get_detection(test_db: Session):
    """Test retrieving a detection"""
    # Create a test detection
    detection = Detection(
        timestamp=datetime.now(UTC),
        class_name="rhino",
        confidence=0.95,
        image_path="/path/to/image.jpg",
        gps_lat=-23.8859,
        gps_lng=31.5205
    )
    test_db.add(detection)
    test_db.commit()

    # Retrieve the detection
    db_detection = test_db.query(Detection).filter(Detection.id == detection.id).first()
    assert db_detection is not None
    assert db_detection.class_name == "rhino"
    assert db_detection.confidence == 0.95