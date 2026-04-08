"""Notification service.

MVP:
- Log WhatsApp notifications.

Production:
- Replace with Meta WhatsApp Cloud API.
- Add retries and delivery receipts.
"""

# Import logging
import logging

# Create module logger
logger = logging.getLogger("exportos.notifier")


def send_whatsapp(phone_number: str, message: str) -> None:
    """Send a WhatsApp message (mocked)."""

    # Log the message instead of sending
    logger.info("[MOCK_WHATSAPP] to=%s message=%s", phone_number, message)
