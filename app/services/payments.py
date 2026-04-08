"""Payment link generation + FX transparency (MVP).

MVP:
- Generate fake payment link
- Compute expected INR using static FX

Production:
- Replace with real payment gateway
- Handle webhooks
"""

# Import uuid for link token
import uuid


def get_fx_rate(currency: str) -> float:
    """Return a mocked FX rate to INR."""

    # Hard-coded rates for MVP
    rates = {"AED": 22.7, "USD": 83.0, "EUR": 90.0}

    # Return known rate or fallback
    return rates.get(currency.upper(), 80.0)


def create_payment_link(shipment_id: str) -> str:
    """Create a fake payment link for a shipment."""

    # Random token
    token = uuid.uuid4().hex

    # Return fake URL
    return f"https://payments.example.com/pay/{shipment_id}/{token}"
