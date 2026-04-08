"""HS Code Suggestion Engine (MVP).

For MVP we implement a deterministic rule-based mapper.
Later, you can replace/augment with ML or a curated HS knowledge base.
"""

# Import typing
from typing import Tuple, List


def suggest_hs(description: str) -> Tuple[str, List[str]]:
    """Suggest an HS code and any compliance alerts."""

    # Normalize input
    text = (description or "").lower()

    # Default output
    hs_code = "9999.00"  # Unknown/default
    alerts: List[str] = []  # Compliance alerts for the UI

    # Very simple category-focused rules
    if any(word in text for word in ["textile", "cotton", "handwoven", "fabric"]):
        hs_code = "6304.92"  # Example: textile furnishing articles
    elif any(word in text for word in ["handicraft", "wood", "carving", "craft"]):
        hs_code = "4420.10"  # Example: wooden marquetry articles
    elif any(word in text for word in ["ceramic", "pottery", "terracotta"]):
        hs_code = "6913.90"  # Example: ceramic ornamental articles

    # Tiny compliance hook
    if "ivory" in text:
        alerts.append("Restricted: ivory-related items may be prohibited.")

    # Return result
    return hs_code, alerts
