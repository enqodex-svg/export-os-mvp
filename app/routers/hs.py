"""HS code router."""

# Import FastAPI router
from fastapi import APIRouter

# Import schemas
from app.schemas import HSSuggestRequest, HSSuggestResponse

# Import HS engine
from app.services.hs_engine import suggest_hs

# Create router
router = APIRouter()


@router.post("/suggest", response_model=HSSuggestResponse)
def suggest(payload: HSSuggestRequest) -> HSSuggestResponse:
    """Suggest HS code based on description."""

    # Call engine
    hs_code, alerts = suggest_hs(payload.description)

    # Return
    return HSSuggestResponse(hs_code=hs_code, alerts=alerts)
