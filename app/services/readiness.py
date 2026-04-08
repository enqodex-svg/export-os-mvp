"""Export readiness scoring.

Goal:
- Reduce anxiety by showing a clear progress metric.
- Provide actionable missing steps.

MVP scoring approach:
- Add points for each critical step completed.
- Return score + missing items.
"""

# Import typing
from typing import List, Tuple

# Import models for typing
from app.db.models import Product, User


def compute_readiness(user: User, product: Product) -> Tuple[int, List[str]]:
    """Compute readiness score (0-100) and missing checklist."""

    # Score accumulator
    score = 0

    # Missing checklist
    missing: List[str] = []

    # Name
    if product.name:
        score += 15
    else:
        missing.append("Product name")

    # Description
    if product.description:
        score += 10
    else:
        missing.append("Product description")

    # Weight
    if product.weight_kg is not None:
        score += 15
    else:
        missing.append("Product weight")

    # Dimensions
    if all(v is not None for v in [product.length_cm, product.width_cm, product.height_cm]):
        score += 15
    else:
        missing.append("Product dimensions")

    # HS code
    if product.hs_code:
        score += 15
    else:
        missing.append("HS code")

    # IEC number (required eventually)
    if user.iec_number:
        score += 15
    else:
        missing.append("IEC number")

    # GST number (optional)
    if user.gst_number:
        score += 5

    # Clamp to 100
    score = min(score, 100)

    # Return computed values
    return score, missing
