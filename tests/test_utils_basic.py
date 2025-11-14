"""Basic tests for utility functions"""
from utils import create_test_image

def test_create_image():
    """Test basic image creation"""
    img_bytes = create_test_image(width=100, height=100)
    assert img_bytes is not None
    assert hasattr(img_bytes, 'getvalue')
    assert len(img_bytes.getvalue()) > 0