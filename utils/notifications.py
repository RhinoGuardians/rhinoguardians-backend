"""
Notifications Module

This module handles sending alerts through various channels (SMS, email)
when rhino detections occur in the system.
"""

from typing import List, Optional
from datetime import datetime
from database.models import Alert
from typing import Optional
import os
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import APIRouter

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.post("/test")
async def test_notification(payload: dict):
    return {"status": "ok", "message": payload.get("message")}

class NotificationService:
    """
    Lightweight notification dispatcher (placeholder).
    Implemented as async to match route usage (await notification_service.send_alert(...)).
    """

    async def send_alert(
        self,
        alert: Optional["Alert"] = None,
        recipient: Optional[str] = None,
        message: Optional[str] = None,
        alert_id: Optional[str] = None,
    ) -> bool:
        """
        Dispatch an alert notification.

        Accepts:
        - send_alert(alert=<Alert>, recipient="...", message="...") or
        - send_alert(alert_id="RG-xxxx", recipient="...")

        Returns True on success. Currently logs and succeeds.
        """
        try:
            # Resolve alert_id from Alert object if not provided
            if not alert_id and alert is not None:
                alert_id = getattr(alert, "alert_id", None) or getattr(alert, "id", None)

            if not alert_id:
                alert_id = "RG-unknown"

            if not recipient:
                recipient = os.getenv("EMAIL_FROM", "alerts@rhinoguardians.ai")

            if not message:
                message = f"Alert {alert_id} triggered."

            logger.info(f"[Notification] alert_id={alert_id} recipient={recipient} msg={message}")
            # TODO: integrate Twilio/SendGrid here using SMS_API_KEY/EMAIL_FROM
            return True
        except Exception as exc:
            logger.exception("Failed to send alert notification: %s", exc)
            return False
    
    async def _send_sms(self, message: str, recipients: List[str]) -> bool:
        """
        Send SMS alerts using configured SMS gateway.
        To be implemented with specific SMS provider (e.g., Twilio).
        """
        if not self.sms_api_key or not recipients:
            return False
            
        try:
            # TODO: Implement SMS sending logic
            # For now, just log the message
            print(f"SMS would be sent to {recipients}: {message}")
            return True
        except Exception as e:
            print(f"Error sending SMS: {e}")
            return False
    
    async def _send_email(
        self,
        message: str,
        recipients: List[str],
        image_url: Optional[str] = None
    ) -> bool:
        """Send email alerts using configured SMTP server."""
        if not recipients:
            return False
            
        try:
            for recipient in recipients:
                msg = MIMEMultipart()
                msg['From'] = self.email_from
                msg['To'] = recipient
                msg['Subject'] = "RhinoGuardians Alert"
                
                body = message
                if image_url:
                    body += f"\n\nView Image: {image_url}"
                    
                msg.attach(MIMEText(body, 'plain'))
                
                with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                    server.starttls()
                    if self.email_password:
                        server.login(self.email_from, self.email_password)
                    server.send_message(msg)
                    
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
            
    def _format_message(
        self,
        message: str,
        detection_id: int,
        image_url: Optional[str] = None,
        coordinates: Optional[tuple] = None
    ) -> str:
        """Format a complete alert message with all relevant information."""
        formatted_msg = [
            f"RHINO ALERT #{detection_id}",
            f"Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}",
            f"Message: {message}"
        ]
        
        if coordinates:
            lat, lng = coordinates
            formatted_msg.append(f"Location: {lat}, {lng}")
            
        if image_url:
            formatted_msg.append(f"Image: {image_url}")
            
        return "\n".join(formatted_msg)
    
    def _is_phone_number(self, recipient: str) -> bool:
        """Check if a recipient string looks like a phone number."""
        return recipient.replace('+', '').replace('-', '').isdigit()
    
    def _is_email(self, recipient: str) -> bool:
        """Check if a recipient string looks like an email address."""
        return '@' in recipient and '.' in recipient.split('@')[1]


# Initialize the notification service
notification_service = NotificationService()


async def send_alert_notification(alert: Alert) -> bool:
    """
    Send a notification for an alert through configured channels.
    
    Args:
        alert (Alert): The alert object to send notification for
        
    Returns:
        bool: True if notification was sent successfully
    """
    # TODO: In production, load recipients from configuration/database
    test_recipients = [
        "alerts@rhinoguardians.ai",  # Email
        "+1234567890"  # Phone
    ]
    
    message = alert.message or f"Alert #{alert.id} for Detection #{alert.detection_id}"
    
    return await notification_service.send_alert(
        message=message,
        recipients=test_recipients,
        detection_id=alert.detection_id
        # TODO: Add image_url and coordinates when available
    )