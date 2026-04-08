"""Payments router.

MVP:
- Create payment link
- Fetch payment status

Production:
- Real gateway integration
- Webhooks
"""

# Import FastAPI
from fastapi import APIRouter, Depends, HTTPException

# Import SQLAlchemy
from sqlalchemy.orm import Session

# Import DB dependency
from app.db.session import get_db

# Import models
from app.db.models import Payment, Shipment

# Import schemas
from app.schemas import PaymentCreateRequest, PaymentOut

# Import payment services
from app.services.payments import create_payment_link, get_fx_rate

# Create router
router = APIRouter()


@router.post("/create-link", response_model=PaymentOut)
def create_link(payload: PaymentCreateRequest, db: Session = Depends(get_db)) -> PaymentOut:
    """Create a payment link for a shipment."""

    # Validate shipment exists
    shipment = db.query(Shipment).filter(Shipment.id == payload.shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")

    # FX rate
    fx = get_fx_rate(payload.currency)

    # Expected INR
    expected_inr = round(payload.amount_foreign * fx, 2)

    # Payment link
    link = create_payment_link(payload.shipment_id)

    # Create row
    p = Payment(
        shipment_id=payload.shipment_id,
        amount_foreign=payload.amount_foreign,
        currency=payload.currency,
        expected_inr=expected_inr,
        status="pending",
        payment_link=link,
    )

    # Persist
    db.add(p)
    db.commit()
    db.refresh(p)

    # Return
    return PaymentOut(
        id=p.id,
        shipment_id=p.shipment_id,
        amount_foreign=p.amount_foreign,
        currency=p.currency,
        expected_inr=p.expected_inr,
        status=p.status,
        payment_link=p.payment_link,
    )


@router.get("/{payment_id}", response_model=PaymentOut)
def get_payment(payment_id: str, db: Session = Depends(get_db)) -> PaymentOut:
    """Fetch payment by ID."""

    # Fetch
    p = db.query(Payment).filter(Payment.id == payment_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Payment not found")

    # Return
    return PaymentOut(
        id=p.id,
        shipment_id=p.shipment_id,
        amount_foreign=p.amount_foreign,
        currency=p.currency,
        expected_inr=p.expected_inr,
        status=p.status,
        payment_link=p.payment_link,
    )
