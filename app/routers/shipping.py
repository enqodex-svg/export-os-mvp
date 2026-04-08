"""Shipping router.

Endpoints:
- /quote
- /book
- /{shipment_id}/track

Integrations:
- Uses a courier adapter (mocked) so we can swap real couriers later.
"""

# Import FastAPI tools
from fastapi import APIRouter, Depends, HTTPException

# Import SQLAlchemy session
from sqlalchemy.orm import Session

# Import DB dependency
from app.db.session import get_db

# Import models
from app.db.models import Shipment, Product, User

# Import schemas
from app.schemas import (
    ShippingQuoteRequest,
    ShippingQuoteOption,
    ShippingBookRequest,
    ShipmentOut,
    TrackingOut,
    TrackingEvent,
)

# Import courier adapter
from app.services.courier import MockCourierAdapter

# Import notifier
from app.services.notifier import send_whatsapp

# Create router
router = APIRouter()

# Create adapter instance
courier_adapter = MockCourierAdapter()


@router.post("/quote", response_model=list[ShippingQuoteOption])
def quote(payload: ShippingQuoteRequest) -> list[ShippingQuoteOption]:
    """Return quote options."""

    # Query adapter
    options = courier_adapter.quote(
        weight_kg=payload.weight_kg,
        dims_cm=[payload.length_cm, payload.width_cm, payload.height_cm],
        incoterm=payload.incoterm,
    )

    # Map to response models
    return [ShippingQuoteOption(**o) for o in options]


@router.post("/book", response_model=ShipmentOut)
def book(payload: ShippingBookRequest, db: Session = Depends(get_db)) -> ShipmentOut:
    """Book a shipment."""

    # Validate product
    product = db.query(Product).filter(Product.id == payload.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Validate user
    user = db.query(User).filter(User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create tracking
    tracking = courier_adapter.book(payload.courier, payload.service_type)

    # Compute a simplistic cost (placeholder)
    cost_inr = 3500.0

    # Create shipment
    shipment = Shipment(
        user_id=user.id,
        product_id=product.id,
        destination_country=payload.destination_country,
        courier=payload.courier,
        service_type=payload.service_type,
        incoterm=payload.incoterm,
        pickup_address=payload.pickup_address,
        tracking_number=tracking,
        status="pickup",
        cost_inr=cost_inr,
    )

    # Persist
    db.add(shipment)
    db.commit()
    db.refresh(shipment)

    # Notify via WhatsApp (mock)
    send_whatsapp(user.phone_number, f"Pickup confirmed. Tracking: {tracking}")

    # Return
    return ShipmentOut(
        id=shipment.id,
        tracking_number=shipment.tracking_number,
        status=shipment.status,
        cost_inr=shipment.cost_inr,
    )


@router.get("/{shipment_id}/track", response_model=TrackingOut)
def track(shipment_id: str, db: Session = Depends(get_db)) -> TrackingOut:
    """Track a shipment."""

    # Fetch shipment
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")

    # Adapter tracking
    info = courier_adapter.track(shipment.tracking_number)

    # Map timeline
    timeline = [TrackingEvent(**e) for e in info["timeline"]]

    # Return
    return TrackingOut(
        tracking_number=info["tracking_number"],
        status=info["status"],
        timeline=timeline,
    )
