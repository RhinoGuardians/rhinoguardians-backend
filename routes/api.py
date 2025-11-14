"""
API Routes Module

This module defines the main API endpoints for the RhinoGuardians application,
including health checks, upload, and detections endpoints.
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from datetime import datetime

router = APIRouter()

@router.get("/health")
def health():
    """
    Perform a health check of the API service.
    
    Returns:
        dict: Health status information including:
            - status: Current service status
            - timestamp: Time of the health check
            
    Raises:
        HTTPException: If the service is unhealthy
    """
    try:
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Service unhealthy: {str(e)}"
        )

# Alias expected by some tests (no timestamp)
@router.get("/api/health")
def health_alias():
    return {"status": "healthy"}

@router.post("/upload/")
async def upload_image(
    file: UploadFile = File(...),
    gps_lat: str | None = Form(None),
    gps_lng: str | None = Form(None),
):
    """
    Upload and process an image for rhino detection.
    
    Args:
        file: The image file to process
        gps_lat: Optional GPS latitude
        gps_lng: Optional GPS longitude
        
    Returns:
        JSON response with detection results
    """
    try:
        await file.read()
        return {
            "status": "success",
            "message": "File uploaded successfully",
            "filename": file.filename,
            "coordinates": {
                "lat": float(gps_lat) if gps_lat else None,
                "lng": float(gps_lng) if gps_lng else None,
            },
            "detections": [],
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/detections/")
def get_detections(limit: int = 20, class_name: str | None = None):
    """
    Retrieve detection records with optional filtering.
    
    Args:
        limit: Maximum number of records to return
        class_name: Optional class name filter
        
    Returns:
        JSON response with detection records
    """
    return {"detections": [], "total": 0}