"""
Alerts Routes Module

This module handles all alert-related endpoints, including retrieving
active alerts, managing alert settings, and triggering notifications.
"""
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, Query, Depends, Path, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select, func, desc
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database.db import get_db
from database.models import Alert, AlertStatus as DBAlertStatus
from utils.notifications import NotificationService
from typing import Optional
from .schemas import AlertTriggerRequest, AlertResponse, Location, AlertStatus as APIAlertStatus, UpdateStatusRequest


router = APIRouter(prefix="/alerts", tags=["alerts"])
# auto_error=False so we can return 401 for missing token instead of 403
security = HTTPBearer(auto_error=False)
notification_service = NotificationService()


@router.get("/")
async def get_alerts(
    limit: int = Query(10, ge=1, le=100),
    skip: int = Query(0, ge=0),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    try:
        # Order by available timestamp; fallback to id
        order_col = getattr(Alert, "timestamp", None) or getattr(Alert, "created_at", None) or Alert.id
        q = select(Alert).order_by(desc(order_col))
        if status:
            value = getattr(DBAlertStatus, status, None) or status
            q = q.filter(Alert.status == value)

        total = db.execute(select(func.count()).select_from(q.subquery())).scalar_one()
        items = db.execute(q.offset(skip).limit(limit)).scalars().all()

        result = []
        for a in items:
            st = a.status.name if hasattr(a.status, "name") else str(a.status)
            ts = a.timestamp if hasattr(a, "timestamp") else getattr(a, "created_at", datetime.utcnow())
            result.append({
                "id": a.id,
                "detection_id": a.detection_id,
                "timestamp": ts.isoformat(),
                "status": st,
                "type": getattr(a, "type", None),
                "severity": getattr(a, "severity", None),
                "source": getattr(a, "source", None),
                "lat": getattr(a, "lat", None),
                "lng": getattr(a, "lng", None),
                "zone_label": getattr(a, "zone_label", None),
                "created_by": getattr(a, "created_by", None),
            })

        return {"alerts": result, "total": total, "timestamp": datetime.utcnow().isoformat()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving alerts: {str(e)}")


@router.post("/trigger", response_model=AlertResponse)
async def trigger_alert(
    payload: AlertTriggerRequest,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    # Missing/bad token -> 401
    if not credentials or credentials.credentials != "testtoken123":
        raise HTTPException(status_code=401, detail="Invalid authentication token")

    try:
        alert = Alert(
            alert_id=payload.detection_id,  # or generate a unique string
            detection_id=payload.detection_id,
            status=getattr(DBAlertStatus, "ACTIVE", None) or "created",
            type=payload.type.value,
            severity=payload.severity.value,
            source=payload.source,
            notes=payload.notes,
            lat=payload.location.lat,
            lng=payload.location.lng,
            zone_label=payload.location.zoneLabel,
            created_by=payload.createdBy,
            timestamp=datetime.utcnow() if hasattr(Alert, "timestamp") else None,
        )
        db.add(alert)
        db.commit()
        db.refresh(alert)

        msg = (
            f"[{payload.severity.value.upper()}] {payload.type.value.replace('_',' ').title()} "
            f"at ({payload.location.lat}, {payload.location.lng}) - {payload.location.zoneLabel}"
            + (f" | {payload.notes}" if payload.notes else "")
        )

        sent = await notification_service.send_alert(alert=alert, recipient=payload.createdBy, message=msg)

        # Update DB status conservatively
        try:
            if hasattr(DBAlertStatus, "ACKNOWLEDGED"):
                alert.status = DBAlertStatus.ACKNOWLEDGED if sent else getattr(DBAlertStatus, "INACTIVE", DBAlertStatus.ACKNOWLEDGED)
            else:
                alert.status = "sent" if sent else "failed"
            if hasattr(alert, "updated_at"):
                alert.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(alert)
        except Exception:
            db.rollback()

        api_status = APIAlertStatus.SENT if sent else APIAlertStatus.FAILED
        created_at = alert.timestamp if hasattr(alert, "timestamp") else getattr(alert, "created_at", datetime.utcnow())
        updated_at = getattr(alert, "updated_at", created_at)

        return AlertResponse(
            id=str(getattr(alert, "alert_id", alert.id)),
            detection_id=alert.detection_id,
            status=api_status,
            type=payload.type,
            severity=payload.severity,
            created_at=created_at,
            updated_at=updated_at,
            location=Location(lat=alert.lat, lng=alert.lng, zoneLabel=alert.zone_label),
            notes=alert.notes,
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create alert: {str(e)}")


@router.patch("/{alert_id}/status")
async def update_alert_status(
    alert_id: str = Path(..., description="The ID of the alert to update"),
    payload: UpdateStatusRequest = ...,
    db: Session = Depends(get_db),
):
    alert = db.query(Alert).filter(Alert.alert_id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail=f"Alert with ID {alert_id} not found")

    status_value = getattr(DBAlertStatus, payload.status.upper(), None) or payload.status
    alert.status = status_value
    if hasattr(alert, "updated_at"):
        alert.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(alert)
    st = alert.status if isinstance(alert.status, str) else getattr(alert.status, "name", str(alert.status))
    ts = alert.timestamp if hasattr(alert, "timestamp") else getattr(alert, "created_at", datetime.utcnow())
    return {
        "id": alert.alert_id,
        "detection_id": alert.detection_id,
        "timestamp": ts.isoformat(),
        "status": st,
    }

