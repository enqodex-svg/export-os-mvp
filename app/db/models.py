"""Database models.

Everything is heavily commented to support learning and maintainability.

NOTE:
- UUIDs are stored as strings for maximum portability between Postgres/SQLite.
"""

# Import datetime for timestamps
import datetime as dt

# Import UUID utilities
import uuid

# Import SQLAlchemy columns/types
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Float, Text

# Import ORM relationship
from sqlalchemy.orm import relationship

# Import Base class
from app.db.session import Base


class User(Base):
    """Represents an exporting seller/user."""

    # Table name in DB
    __tablename__ = "users"

    # Primary key UUID stored as string
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # Phone number is the primary login identifier
    phone_number = Column(String, unique=True, index=True, nullable=False)

    # Optional display name
    name = Column(String, nullable=True)

    # Optional IEC number (asked only when required)
    iec_number = Column(String, nullable=True)

    # Optional GST number
    gst_number = Column(String, nullable=True)

    # Creation timestamp
    created_at = Column(DateTime, default=dt.datetime.utcnow, nullable=False)

    # Relationship to products
    products = relationship("Product", back_populates="user")

    # Relationship to shipments
    shipments = relationship("Shipment", back_populates="user")


class Product(Base):
    """Represents a product listed by the exporter."""

    # Table name
    __tablename__ = "products"

    # Primary key UUID
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # Owning user
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)

    # Product name
    name = Column(String, nullable=False)

    # Product description (used for HS suggestion)
    description = Column(Text, nullable=True)

    # Declared value
    declared_value = Column(Float, nullable=False, default=0.0)

    # Currency for declared value
    currency = Column(String, nullable=False, default="INR")

    # Weight in kilograms
    weight_kg = Column(Float, nullable=True)

    # Dimensions in centimeters
    length_cm = Column(Float, nullable=True)
    width_cm = Column(Float, nullable=True)
    height_cm = Column(Float, nullable=True)

    # Suggested HS code
    hs_code = Column(String, nullable=True)

    # Readiness score 0-100
    readiness_score = Column(Integer, nullable=False, default=0)

    # Status for UI
    status = Column(String, nullable=False, default="draft")

    # Creation timestamp
    created_at = Column(DateTime, default=dt.datetime.utcnow, nullable=False)

    # Relationship to user
    user = relationship("User", back_populates="products")

    # Relationship to shipments
    shipments = relationship("Shipment", back_populates="product")


class Shipment(Base):
    """Represents a booked export shipment."""

    # Table name
    __tablename__ = "shipments"

    # Primary key
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # Owning user
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)

    # Linked product
    product_id = Column(String, ForeignKey("products.id"), nullable=False, index=True)

    # Destination country (MVP: UAE)
    destination_country = Column(String, nullable=False, default="UAE")

    # Courier name
    courier = Column(String, nullable=False)

    # Service type: express/economy
    service_type = Column(String, nullable=False)

    # Incoterm: DDP/DDU
    incoterm = Column(String, nullable=False)

    # Pickup address
    pickup_address = Column(Text, nullable=False)

    # Tracking number
    tracking_number = Column(String, nullable=True)

    # Status
    status = Column(String, nullable=False, default="created")

    # Cost in INR
    cost_inr = Column(Float, nullable=False, default=0.0)

    # Created timestamp
    created_at = Column(DateTime, default=dt.datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="shipments")
    product = relationship("Product", back_populates="shipments")
    documents = relationship("Document", back_populates="shipment")
    payments = relationship("Payment", back_populates="shipment")


class Document(Base):
    """Represents a generated document (PDF)."""

    # Table name
    __tablename__ = "documents"

    # Primary key
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # Owning shipment
    shipment_id = Column(String, ForeignKey("shipments.id"), nullable=False, index=True)

    # Document type
    type = Column(String, nullable=False)

    # File URL / path
    file_url = Column(String, nullable=False)

    # Created timestamp
    created_at = Column(DateTime, default=dt.datetime.utcnow, nullable=False)

    # Relationship
    shipment = relationship("Shipment", back_populates="documents")


class Payment(Base):
    """Represents a payment record for a shipment."""

    # Table name
    __tablename__ = "payments"

    # Primary key
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # Owning shipment
    shipment_id = Column(String, ForeignKey("shipments.id"), nullable=False, index=True)

    # Foreign amount
    amount_foreign = Column(Float, nullable=False, default=0.0)

    # Currency
    currency = Column(String, nullable=False, default="AED")

    # Expected INR settlement
    expected_inr = Column(Float, nullable=False, default=0.0)

    # Status
    status = Column(String, nullable=False, default="pending")

    # Payment link
    payment_link = Column(String, nullable=False)

    # Created timestamp
    created_at = Column(DateTime, default=dt.datetime.utcnow, nullable=False)

    # Relationship
    shipment = relationship("Shipment", back_populates="payments")
