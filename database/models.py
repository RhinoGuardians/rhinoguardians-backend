"""
Database Models Module

This module defines the SQLAlchemy ORM models for the RhinoGuardians application.
It includes models for storing detection results and their associated metadata.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime
import enum


class Base(DeclarativeBase):
    """Base class for all database models."""
    pass


class AlertStatus(str, enum.Enum):
    """
    Enum for alert statuses.
    """
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
    INACTIVE = "inactive"


class Detection(Base):
    """
    Detection model for storing rhino detection results.
    
    Attributes:
        id (int): Primary key
        timestamp (datetime): When the detection occurred
        class_name (str): Type of object detected (e.g., 'rhino')
        confidence (float): Detection confidence score (0-1)
        image_path (str): Path to the stored image
        gps_lat (float): GPS latitude of detection
        gps_lng (float): GPS longitude of detection
    """
    __tablename__ = 'detections'
    
    id = Column(Integer, primary_key=True, index=True, 
               comment='Unique identifier for the detection')
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow,
                      comment='Timestamp when the detection occurred')
    class_name = Column(String, nullable=False,
                       comment='Type of object detected')
    confidence = Column(Float, nullable=False,
                       comment='Confidence score of detection')
    image_path = Column(String, nullable=False,
                     comment='Path to stored image')

    # Relationship with alerts
    alerts = relationship("Alert", back_populates="detection", cascade="all, delete-orphan")
    gps_lat = Column(Float, nullable=True,
                     comment='GPS latitude of the detection')
    gps_lng = Column(Float, nullable=True,
                     comment='GPS longitude of the detection')


class Alert(Base):
    """
    Alert model for tracking notifications and status of critical detections.
    
    Attributes:
        id (int): Primary key
        detection_id (int): Foreign key to the associated detection
        timestamp (datetime): When the alert was created
        status (AlertStatus): Current status of the alert
        type (str): Type of alert (e.g., poacher_suspected)
        severity (str): Alert severity level
        source (str): Source of the alert (e.g., camera_trap)
        notes (str): Optional operator notes
        lat (float): Latitude of alert location
        lng (float): Longitude of alert location
        zone_label (str): Label of the zone where alert was triggered
        created_by (str): Operator who created the alert
        notification_sent (bool): Whether notification was sent
        notification_timestamp (datetime): When notification was sent
        message (str): Alert message/description
    """
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True,
                comment='Unique identifier for the alert')
    alert_id = Column(String, unique=True, nullable=False)  # Required for PATCH
    detection_id = Column(String, 
                         ForeignKey('detections.id', ondelete='CASCADE'),
                         nullable=False,
                         comment='ID of the associated detection')
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow,
                      comment='When the alert was created')
    status = Column(Enum(AlertStatus), nullable=False, default=AlertStatus.ACTIVE,
                   comment='Current status of the alert')
    type = Column(String, nullable=False,
                 comment='Type of alert (e.g., poacher_suspected)')
    severity = Column(String, nullable=False,
                     comment='Alert severity level')
    source = Column(String, nullable=False,
                   comment='Source of the alert (e.g., camera_trap)')
    notes = Column(String, nullable=True,
                  comment='Optional operator notes')
    lat = Column(Float, nullable=True,
                comment='Latitude of alert location')
    lng = Column(Float, nullable=True,
                comment='Longitude of alert location')
    zone_label = Column(String, nullable=True,
                       comment='Label of the zone where alert was triggered')
    created_by = Column(String, nullable=True,
                       comment='Operator who created the alert')
    notification_sent = Column(Integer, default=0,
                             comment='Whether notification was sent (0=no, 1=yes)')
    notification_timestamp = Column(DateTime, nullable=True,
                                  comment='When notification was sent')
    message = Column(String, nullable=True,
                    comment='Alert message or description')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow,
                       comment='When the alert was last updated')
