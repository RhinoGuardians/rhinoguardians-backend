"""Test utilities for image creation and processing"""
from PIL import Image
import io

def create_test_image(width=640, height=480, color='white'):
    """Create a test image for unit tests"""
    img = Image.new('RGB', (width, height), color=color)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    return img_byte_arr

def create_test_image_file(filepath, width=640, height=480, color='white'):
    """Create a test image and save it to a file"""
    img = Image.new('RGB', (width, height), color=color)
    img.save(filepath, format='JPEG')