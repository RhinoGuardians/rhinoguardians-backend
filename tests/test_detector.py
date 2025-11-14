"""Test the YOLO detector"""
import os
import pytest
from PIL import Image
import numpy as np
from models.yolo_detector import YoloDetector
from utils import create_test_image, create_test_image_file

@pytest.fixture
def test_image(tmp_path):
    """Create a test image for detection"""
    image_path = tmp_path / "test_image.jpg"
    # Create a blank image
    img = Image.new('RGB', (640, 480), color='white')
    img.save(image_path)
    return str(image_path)

def test_yolo_detector_initialization():
    """Test YOLO detector initialization with invalid model path"""
    with pytest.raises(FileNotFoundError):
        YoloDetector("nonexistent_model.pt")

def test_image_detection(test_image):
    """Test image detection (requires model file)"""
    model_path = os.getenv("MODEL_PATH", "./models/yolov5s.pt")
    if not os.path.exists(model_path):
        pytest.skip("Model file not found")
    
    detector = YoloDetector(model_path)
    detections = detector.predict(test_image)
    
    assert isinstance(detections, list)
    for detection in detections:
        assert "box" in detection
        assert "confidence" in detection
        assert "class" in detection
        assert isinstance(detection["confidence"], float)
        assert isinstance(detection["class"], int)