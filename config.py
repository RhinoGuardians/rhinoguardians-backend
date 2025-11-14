"""
Configuration Module

This module manages application-wide configuration settings for the RhinoGuardians
backend. It loads configuration from environment variables with sensible defaults
and provides typed configuration values to the application.

Environment Variables:
    DATABASE_URL: SQLAlchemy database connection string
    MODEL_PATH: Path to the YOLO model weights file
    DEBUG: Enable debug mode (True/False)
    PORT: Server port number
    SMS_API_KEY: API key for SMS notifications
    EMAIL_FROM: Sender email for notifications
"""

import os
from typing import Any, Dict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_env_value(key: str, default: Any = None, required: bool = False) -> Any:
    """
    Get environment variable with validation.
    
    Args:
        key (str): Environment variable name
        default (Any): Default value if not set
        required (bool): Whether the variable is required
        
    Returns:
        Any: The environment variable value
        
    Raises:
        ValueError: If a required variable is missing
    """
    value = os.getenv(key, default)
    if required and value is None:
        raise ValueError(f"Required environment variable {key} is not set")
    return value


# Database configuration
DATABASE_URL = get_env_value(
    'DATABASE_URL',
    'sqlite:///./detections.db',
    required=True
)

# Model configuration
MODEL_PATH = get_env_value(
    'MODEL_PATH',
    './models/yolov5s.pt',
    required=True
)

# Server configuration
DEBUG = get_env_value('DEBUG', 'True').lower() == 'true'
PORT = int(get_env_value('PORT', '8000'))

# Alert configuration
SMS_API_KEY = get_env_value('SMS_API_KEY', '')
EMAIL_FROM = get_env_value(
    'EMAIL_FROM',
    'alerts@rhinoguardians.ai',
    required=True
)