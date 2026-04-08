"""Courier abstraction layer.

MVP:
- Deterministic quotes
- Booking returns a tracking number
- Tracking returns a status timeline

Production:
- Replace mock adapter with provider-specific adapters
- Use webhooks/polling for live tracking
"""

# Import standard libs
import random
import datetime as dt

# Import typing
from typing import List, Dict


class CourierAdapter:
    """Interface for courier integrations."""

    def quote(self, weight_kg: float, dims_cm: List[float], incoterm: str) -> List[Dict]:
        """Return available quote options."""
        raise NotImplementedError

    def book(self, courier: str, service_type: str) -> str:
        """Book shipment and return tracking number."""
        raise NotImplementedError

    def track(self, tracking_number: str) -> Dict:
        """Return tracking status + timeline."""
        raise NotImplementedError


class MockCourierAdapter(CourierAdapter):
    """Mock courier adapter with deterministic pricing logic."""

    def quote(self, weight_kg: float, dims_cm: List[float], incoterm: str) -> List[Dict]:
        """Generate mock quote options."""

        # Base prices per courier
        base = {
            "Aramex": 1500,
            "DHL": 2500,
            "FedEx": 2300,
        }

        # Incoterm multiplier
        incoterm_multiplier = 1.25 if incoterm.upper() == "DDP" else 1.0

        # Volumetric weight approximation
        vol_weight = (dims_cm[0] * dims_cm[1] * dims_cm[2]) / 5000.0

        # Billable weight
        billable = max(weight_kg, vol_weight)

        # Options list
        options: List[Dict] = []

        # Build options
        for courier, b in base.items():
            # Express/economy prices
            express_price = (b + billable * 800) * incoterm_multiplier
            economy_price = (b * 0.8 + billable * 550) * incoterm_multiplier

            # Append express
            options.append(
                {
                    "courier": courier,
                    "service_type": "express",
                    "incoterm": incoterm.upper(),
                    "price_inr": round(express_price, 2),
                    "eta_days": 3,
                }
            )

            # Append economy
            options.append(
                {
                    "courier": courier,
                    "service_type": "economy",
                    "incoterm": incoterm.upper(),
                    "price_inr": round(economy_price, 2),
                    "eta_days": 5,
                }
            )

        # Return
        return options

    def book(self, courier: str, service_type: str) -> str:
        """Create a mock tracking number."""

        # Prefix
        prefix = courier[:2].upper()

        # Random numeric suffix
        suffix = random.randint(10000000, 99999999)

        # Return formatted tracking
        return f"{prefix}{service_type[:1].upper()}-{suffix}"

    def track(self, tracking_number: str) -> Dict:
        """Return a mock tracking timeline."""

        # Steps
        steps = [
            ("pickup", "Pickup confirmed"),
            ("export_customs", "Cleared export customs"),
            ("in_transit", "In transit"),
            ("import_customs", "Cleared import customs"),
            ("delivered", "Delivered"),
        ]

        # Pseudo-random position based on hash
        idx = abs(hash(tracking_number)) % len(steps)

        # Status code
        status_code = steps[idx][0]

        # Current time
        now = dt.datetime.utcnow()

        # Timeline
        timeline = []

        # Populate events up to idx
        for i, (code, label) in enumerate(steps):
            if i <= idx:
                timeline.append(
                    {
                        "code": code,
                        "label": label,
                        "timestamp": (now - dt.timedelta(hours=(idx - i) * 6)).isoformat() + "Z",
                    }
                )

        # Return structure
        return {"tracking_number": tracking_number, "status": status_code, "timeline": timeline}
