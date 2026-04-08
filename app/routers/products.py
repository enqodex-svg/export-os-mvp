"""Product router.

Provides endpoints for:
- Product creation
- Listing
- Readiness score calculation

NOTE:
- Auth is mocked for MVP.
- We auto-create a demo user.
"""

# Import FastAPI tools
from fastapi import APIRouter, Depends, HTTPException

# Import SQLAlchemy session
from sqlalchemy.orm import Session

# Import DB dependency
from app.db.session import get_db

# Import models
from app.db.models import User, Product

# Import schemas
from app.schemas import ProductCreate, ProductOut, ReadinessOut

# Import readiness scoring
from app.services.readiness import compute_readiness

# Import HS engine
from app.services.hs_engine import suggest_hs

# Create router
router = APIRouter()


def _get_or_create_user(db: Session, phone_number: str = "+910000000000") -> User:
    """MVP helper: create a default user if none exists."""

    # Query for user
    user = db.query(User).filter(User.phone_number == phone_number).first()

    # Create if missing
    if not user:
        user = User(phone_number=phone_number, name="Demo User")
        db.add(user)
        db.commit()
        db.refresh(user)

    # Return
    return user


@router.post("/", response_model=ProductOut)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)) -> ProductOut:
    """Create a product for the current user."""

    # Get user (mock)
    user = _get_or_create_user(db)

    # Suggest HS code if description exists
    hs_code = None
    if payload.description:
        hs_code, _alerts = suggest_hs(payload.description)

    # Create Product model
    product = Product(
        user_id=user.id,
        name=payload.name,
        description=payload.description,
        declared_value=payload.declared_value,
        currency=payload.currency,
        weight_kg=payload.weight_kg,
        length_cm=payload.length_cm,
        width_cm=payload.width_cm,
        height_cm=payload.height_cm,
        hs_code=hs_code,
        status="draft",
    )

    # Compute readiness
    score, _missing = compute_readiness(user, product)
    product.readiness_score = score
    product.status = "ready" if score >= 70 else "draft"

    # Persist
    db.add(product)
    db.commit()
    db.refresh(product)

    # Return
    return ProductOut(
        id=product.id,
        user_id=product.user_id,
        name=product.name,
        description=product.description,
        declared_value=product.declared_value,
        currency=product.currency,
        weight_kg=product.weight_kg,
        length_cm=product.length_cm,
        width_cm=product.width_cm,
        height_cm=product.height_cm,
        hs_code=product.hs_code,
        readiness_score=product.readiness_score,
        status=product.status,
        created_at=product.created_at.isoformat() + "Z",
    )


@router.get("/", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)) -> list[ProductOut]:
    """List products for the current user."""

    # Get user
    user = _get_or_create_user(db)

    # Query products
    products = (
        db.query(Product)
        .filter(Product.user_id == user.id)
        .order_by(Product.created_at.desc())
        .all()
    )

    # Map to output
    return [
        ProductOut(
            id=p.id,
            user_id=p.user_id,
            name=p.name,
            description=p.description,
            declared_value=p.declared_value,
            currency=p.currency,
            weight_kg=p.weight_kg,
            length_cm=p.length_cm,
            width_cm=p.width_cm,
            height_cm=p.height_cm,
            hs_code=p.hs_code,
            readiness_score=p.readiness_score,
            status=p.status,
            created_at=p.created_at.isoformat() + "Z",
        )
        for p in products
    ]


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: str, db: Session = Depends(get_db)) -> ProductOut:
    """Fetch a single product."""

    # Query product
    p = db.query(Product).filter(Product.id == product_id).first()

    # Not found
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")

    # Return
    return ProductOut(
        id=p.id,
        user_id=p.user_id,
        name=p.name,
        description=p.description,
        declared_value=p.declared_value,
        currency=p.currency,
        weight_kg=p.weight_kg,
        length_cm=p.length_cm,
        width_cm=p.width_cm,
        height_cm=p.height_cm,
        hs_code=p.hs_code,
        readiness_score=p.readiness_score,
        status=p.status,
        created_at=p.created_at.isoformat() + "Z",
    )


@router.get("/{product_id}/readiness", response_model=ReadinessOut)
def readiness(product_id: str, db: Session = Depends(get_db)) -> ReadinessOut:
    """Compute readiness score and missing items."""

    # Get user
    user = _get_or_create_user(db)

    # Query product
    product = db.query(Product).filter(Product.id == product_id).first()

    # Not found
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Compute
    score, missing = compute_readiness(user, product)

    # Update stored score
    product.readiness_score = score
    product.status = "ready" if score >= 70 else "draft"
    db.commit()

    # Return
    return ReadinessOut(score=score, missing=missing)
