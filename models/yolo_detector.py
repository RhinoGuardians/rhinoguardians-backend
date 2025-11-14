"""
YOLO Object Detection Module

This module provides a wrapper around the YOLOv5 model for object detection.
It handles model loading, image preprocessing, and detection inference with
proper error handling and input validation.
"""

import os
import torch
from PIL import Image
from typing import List, Dict, Union
from pathlib import Path


# Short-circuit detector for tests or environments without YOLO dependencies
if os.getenv("SKIP_YOLO") == "1":
    class YoloDetector:
        def __init__(self, model_path: str | None = None, *_, **__):
            # In tests, skip heavy load but still validate invalid paths if provided
            if model_path and not Path(model_path).exists():
                raise FileNotFoundError(f"Model not found: {model_path}")
            self._stub = True

        def predict(self, image_path: str) -> List[Dict[str, Union[List[float], float, int]]]:
            # Always return empty in stub mode
            return []
else:
    class YoloDetector:
        """
        YOLO object detection model wrapper.

        This class provides an interface to the YOLOv5 model for performing
        object detection on images. It handles model initialization, image
        preprocessing, and inference with proper error handling.

        Attributes:
            model: The loaded YOLOv5 model instance
        """

        def __init__(self, model_path: str):
            """
            Initialize YOLO detector with a model path.

            Args:
                model_path (str): Path to the YOLOv5 model weights file

            Raises:
                FileNotFoundError: If model file doesn't exist
                RuntimeError: If model loading fails

            Notes:
                The model is loaded with force_reload=False for better performance
                when multiple instances are created.
            """
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found: {model_path}")

            try:
                self.model = torch.hub.load(
                    'ultralytics/yolov5',
                    'custom',
                    path=model_path,
                    force_reload=False
                )
                # Set inference parameters
                self.model.conf = 0.25  # Confidence threshold
                self.model.iou = 0.45   # NMS IoU threshold
            except Exception as e:
                raise RuntimeError(f"Failed to load YOLO model: {str(e)}")

        def predict(self, image_path: str) -> List[Dict[str, Union[List[float], float, int]]]:
            """
            Perform object detection on an image.

            Args:
                image_path (str): Path to the input image file

            Returns:
                List[Dict]: List of detections, where each detection is a dictionary:
                    {
                        "box": [x1, y1, x2, y2],  # Bounding box coordinates
                        "confidence": float,        # Detection confidence (0-1)
                        "class": int               # Class ID of detected object
                    }

            Raises:
                FileNotFoundError: If image file doesn't exist
                PIL.UnidentifiedImageError: If image format is not supported
                RuntimeError: If prediction fails

            Notes:
                The function verifies image integrity before processing and
                handles proper resource cleanup.
            """
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image file not found: {image_path}")

            try:
                # Verify image integrity
                img = Image.open(image_path)
                img.verify()  # Verify it's a valid image
                img = Image.open(image_path)  # Reopen (verify closes the file)
            except Exception as e:
                raise RuntimeError(f"Failed to open image: {str(e)}")

            try:
                # Perform inference
                results = self.model(img)
                detections: List[Dict[str, Union[List[float], float, int]]] = []

                # Convert tensor to list and process detections
                for *box, conf, cls in results.xyxy[0].tolist():
                    detections.append({
                        "box": box,          # [x1, y1, x2, y2]
                        "confidence": float(conf),
                        "class": int(cls)
                    })
                return detections

            except Exception as e:
                raise RuntimeError(f"Model prediction failed: {str(e)}")
            finally:
                img.close()  # Ensure image file is closed
