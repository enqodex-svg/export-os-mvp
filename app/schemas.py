"""Pydantic schemas for request/response payloads.

Commented extensively for clarity.
"""

# Import typing helpers
from typing import Optional, List

# Import pydantic base classes
from pydantic import BaseModel, Field


# -------------------------
# Auth schemas
# -------------------------

class OTPRequest(BaseModel):
    """Request schema for starting OTP login."""

    # Phone number including country code (e.g., +91...)
    phone_number: str = Field(..., examples=["+919999999999"])


class OTPVerifyRequest(BaseModel):
    """Request schema for verifying OTP."""

    # Phone number used
    phone_number: str

    # OTP code (MVP uses fixed 123456)
    otp: str


class AuthTokenResponse(BaseModel):
    """Response schema with a mock token."""

    # Token value
    token: str


# -------------------------
# Product schemas
# -------------------------

class ProductCreate(BaseModel):
    """Request schema for creating a product."""

    # Product name
    name: str

    # Product description
    description: Optional[str] = None

    # Declared value
    declared_value: float = 0.0

    # Currency
    currency: str = "INR"

    # Physical properties
    weight_kg: Optional[float] = None
    length_cm: Optional[float] = None
    width_cm: Optional[float] = None
    height_cm: Optional[float] = None


class ProductOut(BaseModel):
    """Response schema for product."""

    id: str
    user_id: str
    name: str
    description: Optional[str] = None
    declared_value: float
    currency: str
    weight_kg: Optional[float] = None
    length_cm: Optional[float] = None
    width_cm: Optional[float] = None
    height_cm: Optional[float] = None
    hs_code: Optional[str] = None
    readiness_score: int
    status: str
    created_at: str


class ReadinessOut(BaseModel):
    """Readiness score output."""

    score: int
    missing: List[str]


# -------------------------
# HS code suggestion schemas
# -------------------------

class HSSuggestRequest(BaseModel):
    """Input for HS code suggestion."""

    description: str


class HSSuggestResponse(BaseModel):
    """HS code suggestion output."""

    hs_code: str
    alerts: List[str]


# -------------------------
# Shipping schemas
# -------------------------

class ShippingQuoteRequest(BaseModel):
    """Request to quote shipping."""

    destination: str = "UAE"
    weight_kg: float
    length_cm: float
    width_cm: float
    height_cm: float
    incoterm: str = "DDU"


class ShippingQuoteOption(BaseModel):
    """Single quote option."""

    courier: str
    service_type: str
    incoterm: str
    price_inr: float
    eta_days: int


class ShippingBookRequest(BaseModel):
    """Request to book a shipment."""

    user_id: str
    product_id: str
    destination_country: str = "UAE"
    courier: str
    service_type: str
    incoterm: str
    pickup_address: str


class ShipmentOut(BaseModel):
    """Shipment response payload."""

    id: str
    tracking_number: str
    status: str
    cost_inr: float


class TrackingEvent(BaseModel):
    """Tracking timeline event."""

    code: str
    label: str
    timestamp: str


class TrackingOut(BaseModel):
    """Tracking response."""

    tracking_number: str
    status: str
    timeline: List[TrackingEvent]


# -------------------------
# Document schemas
# -------------------------

class DocumentOut(BaseModel):
    """Document response."""

    id: str
    shipment_id: str
    type: str
    file_url: str


# -------------------------
# Payment schemas
# -------------------------

class PaymentCreateRequest(BaseModel):
    """Request to create a payment link."""

    shipment_id: str
    amount_foreign: float
    currency: str = "AED"


class PaymentOut(BaseModel):
    """Payment output."""

    id: str
    shipment_id: str
    amount_foreign: float
    currency: str
    expected_inr: float
    status: str
    payment_link: str
