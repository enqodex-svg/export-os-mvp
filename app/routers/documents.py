"""Document generation router.

Generates:
- Commercial Invoice
- Packing List
- Shipping Label

MVP:
- Generates PDFs locally under ./generated

Production:
- Store in object storage (S3/GCS/Azure Blob)
- Add signed URLs
"""

# Import pathlib
import pathlib

# Import FastAPI tools
from fastapi import APIRouter, Depends, HTTPException

# Import SQLAlchemy session
from sqlalchemy.orm import Session

# Import DB dependency
from app.db.session import get_db

# Import models
from app.db.models import Shipment, Product, User, Document

# Import schema
from app.schemas import DocumentOut

# Import PDF generation functions
from app.services.pdfs import generate_invoice_pdf, generate_packing_list_pdf, generate_label_pdf

# Create router
router = APIRouter()

# Generated folder
GENERATED_DIR = pathlib.Path("./generated")


@router.post("/{shipment_id}/generate", response_model=list[DocumentOut])
def generate_documents(shipment_id: str, db: Session = Depends(get_db)) -> list[DocumentOut]:
    """Generate all documents for a shipment."""

    # Ensure directory exists
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)

    # Fetch shipment
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")

    # Fetch related entities
    product = db.query(Product).filter(Product.id == shipment.product_id).first()
    user = db.query(User).filter(User.id == shipment.user_id).first()

    # Validate
    if not product or not user:
        raise HTTPException(status_code=400, detail="Shipment references missing user/product")

    # Output paths
    invoice_path = GENERATED_DIR / f"invoice_{shipment.id}.pdf"
    packing_path = GENERATED_DIR / f"packing_{shipment.id}.pdf"
    label_path = GENERATED_DIR / f"label_{shipment.id}.pdf"

    # Generate files
    generate_invoice_pdf(str(invoice_path), user=user, product=product, shipment=shipment)
    generate_packing_list_pdf(str(packing_path), user=user, product=product, shipment=shipment)
    generate_label_pdf(str(label_path), user=user, product=product, shipment=shipment)

    # Create DB rows (no dedupe for MVP)
    docs = []
    for doc_type, file_path in [
        ("invoice", str(invoice_path)),
        ("packing_list", str(packing_path)),
        ("label", str(label_path)),
    ]:
        d = Document(shipment_id=shipment.id, type=doc_type, file_url=file_path)
        db.add(d)
        docs.append(d)

    # Persist
    db.commit()

    # Refresh for IDs
    for d in docs:
        db.refresh(d)

    # Return
    return [DocumentOut(id=d.id, shipment_id=d.shipment_id, type=d.type, file_url=d.file_url) for d in docs]
