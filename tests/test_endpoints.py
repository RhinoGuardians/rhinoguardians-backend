"""Test the upload and detections endpoints"""
import os
import pytest
from fastapi.testclient import TestClient
from PIL import Image
import io
from datetime import datetime, UTC
from main import app

client = TestClient(app)

@pytest.fixture
def test_image():
    """Create a test image for upload"""
    img = Image.new('RGB', (640, 480), color='white')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    return img_byte_arr

def test_upload_endpoint(test_image):
    """Test uploading an image"""
    files = {
        'file': ('test_image.jpg', test_image, 'image/jpeg')
    }
    data = {
        'gps_lat': '-23.8859',
        'gps_lng': '31.5205'
    }
    response = client.post("/upload/", files=files, data=data)
    assert response.status_code == 200
    json_response = response.json()
    assert "detections" in json_response
    for detection in json_response["detections"]:
        assert "id" in detection
        assert "class_name" in detection
        assert "confidence" in detection

def test_detections_endpoint():
    """Test retrieving detections"""
    response = client.get("/detections/")
    assert response.status_code == 200
    json_response = response.json()
    assert "detections" in json_response