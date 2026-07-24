"""Alert management for temperature monitoring system."""

import logging
import smtplib
from datetime import datetime, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Optional

import requests

from monitor.config import (
    ALERT_EMAIL_ENABLED,
    ALERT_EMAIL_RECIPIENTS,
    ALERT_WEBHOOK_URL,
    TEMPERATURE_CRITICAL,
    TEMPERATURE_WARNING,
    get_temperature_status,
)

logger = logging.getLogger(__name__)


class AlertManager:
    """Manages temperature alerts and notifications."""

    def __init__(self):
        """Initialize alert manager."""
        self._alert_history: list[dict[str, Any]] = []
        self._last_alert: Optional[dict[str, Any]] = None
        self._cooldown_seconds = 300  # 5 minutes between repeated alerts
        self._last_alert_time: Optional[datetime] = None
        logger.info("Alert manager initialized")

    def check_temperature(self, temperature: float, device_id: str, location: dict[str, Any]) -> Optional[dict[str, Any]]:
        """
        Check temperature and trigger alerts if needed.

        Args:
            temperature: Current temperature in Celsius
            device_id: Device identifier
            location: Location information

        Returns:
            Alert dictionary if alert triggered, None otherwise
        """
        status, color = get_temperature_status(temperature)

        if status == "ok":
            return None

        # Check cooldown
        now = datetime.now(timezone.utc)
        if self._last_alert_time:
            elapsed = (now - self._last_alert_time).total_seconds()
            if elapsed < self._cooldown_seconds:
                logger.debug(f"Alert cooldown active ({elapsed:.0f}s / {self._cooldown_seconds}s)")
                return None

        # Create alert
        alert = {
            "timestamp": now.isoformat(),
            "device_id": device_id,
            "temperature": temperature,
            "status": status,
            "color": color,
            "location": location,
            "message": self._create_alert_message(temperature, status, location),
        }

        # Store alert
        self._alert_history.append(alert)
        self._last_alert = alert
        self._last_alert_time = now

        # Send notifications
        self._send_notifications(alert)

        logger.warning(f"Alert triggered: {alert['message']}")
        return alert

    def _create_alert_message(self, temperature: float, status: str, location: dict[str, Any]) -> str:
        """
        Create human-readable alert message.

        Args:
            temperature: Temperature in Celsius
            status: Alert status
            location: Location information

        Returns:
            Alert message string
        """
        room = location.get("room", "Unknown")
        rack = location.get("rack_id", "")

        if status == "critical":
            level = "CRITICAL"
        else:
            level = "WARNING"

        message = f"[{level}] Temperature {temperature:.1f}°C in {room}"
        if rack:
            message += f" (Rack: {rack})"

        return message

    def _send_notifications(self, alert: dict[str, Any]) -> None:
        """
        Send alert notifications through configured channels.

        Args:
            alert: Alert dictionary
        """
        # Send email notification
        if ALERT_EMAIL_ENABLED and ALERT_EMAIL_RECIPIENTS:
            self._send_email_alert(alert)

        # Send webhook notification
        if ALERT_WEBHOOK_URL:
            self._send_webhook_alert(alert)

    def _send_email_alert(self, alert: dict[str, Any]) -> None:
        """
        Send email alert notification.

        Args:
            alert: Alert dictionary
        """
        try:
            # Email configuration from environment
            import os

            smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
            smtp_port = int(os.getenv("SMTP_PORT", "587"))
            smtp_username = os.getenv("SMTP_USERNAME", "")
            smtp_password = os.getenv("SMTP_PASSWORD", "")

            if not smtp_username or not smtp_password:
                logger.warning("SMTP credentials not configured")
                return

            # Create message
            msg = MIMEMultipart()
            msg["From"] = smtp_username
            msg["To"] = ALERT_EMAIL_RECIPIENTS
            msg["Subject"] = f"IoT Temperature Alert - {alert['status'].upper()}"

            body = f"""
            <html>
            <body>
                <h2>Temperature Alert</h2>
                <p><strong>Status:</strong> {alert['status'].upper()}</p>
                <p><strong>Temperature:</strong> {alert['temperature']:.1f}°C</p>
                <p><strong>Device:</strong> {alert['device_id']}</p>
                <p><strong>Room:</strong> {alert['location'].get('room', 'Unknown')}</p>
                <p><strong>Time:</strong> {alert['timestamp']}</p>
                <hr>
                <p><em>This is an automated alert from your IoT Temperature Monitor.</em></p>
            </body>
            </html>
            """

            msg.attach(MIMEText(body, "html"))

            # Send email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.send_message(msg)

            logger.info(f"Email alert sent to {ALERT_EMAIL_RECIPIENTS}")
        except Exception as e:
            logger.error(f"Failed to send email alert: {e}")

    def _send_webhook_alert(self, alert: dict[str, Any]) -> None:
        """
        Send webhook alert notification.

        Args:
            alert: Alert dictionary
        """
        try:
            payload = {
                "text": alert["message"],
                "alert": {
                    "status": alert["status"],
                    "temperature": alert["temperature"],
                    "device_id": alert["device_id"],
                    "location": alert["location"],
                    "timestamp": alert["timestamp"],
                },
            }

            response = requests.post(
                ALERT_WEBHOOK_URL,
                json=payload,
                timeout=10,
            )

            if response.ok:
                logger.info("Webhook alert sent successfully")
            else:
                logger.warning(f"Webhook alert failed: {response.status_code}")
        except Exception as e:
            logger.error(f"Failed to send webhook alert: {e}")

    def get_history(self, limit: int = 50) -> list[dict[str, Any]]:
        """
        Get alert history.

        Args:
            limit: Maximum number of alerts to return

        Returns:
            List of alert dictionaries
        """
        return self._alert_history[-limit:]

    def get_latest_alert(self) -> Optional[dict[str, Any]]:
        """
        Get the most recent alert.

        Returns:
            Latest alert dictionary or None
        """
        return self._last_alert

    def clear_history(self) -> None:
        """Clear alert history."""
        self._alert_history.clear()
        logger.info("Alert history cleared")
