"""
API Schemas Module

This module defines Pydantic models for request/response validation
in the RhinoGuardians API.
"""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime


class AlertSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertType(str, Enum):
    POACHER_SUSPECTED = "poacher_suspected"
    VEHICLE_SUSPECTED = "vehicle_suspected"
    RHINO_SIGHTING = "rhino_sighting"
    OTHER = "other"


class AlertStatus(str, Enum):
    CREATED = "created"
    SENT = "sent"
    ACKNOWLEDGED = "acknowledged"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    FAILED = "failed"
    EXPIRED = "expired"


class Location(BaseModel):
    lat: float = Field(..., description="Latitude of the alert location")
    lng: float = Field(..., description="Longitude of the alert location")
    zoneLabel: str = Field(..., description="Label of the zone where alert was triggered")


class AlertTriggerRequest(BaseModel):
    detection_id: str
    type: AlertType
    severity: AlertSeverity
    source: str
    notes: Optional[str] = None
    location: Location
    createdBy: str


class AlertResponse(BaseModel):
    id: str = Field(..., description="Alert ID (format: RG-XXX or DB id)")
    detection_id: str = Field(..., description="ID of the triggering detection")
    status: AlertStatus = Field(..., description="Current alert status")
    type: AlertType = Field(..., description="Type of alert")
    severity: AlertSeverity = Field(..., description="Severity level")
    created_at: datetime = Field(..., description="Alert creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    location: Location = Field(..., description="Location information")
    notes: Optional[str] = Field(None, description="Optional notes")

    class Config:
        from_attributes = True


class UpdateStatusRequest(BaseModel):
    status: str