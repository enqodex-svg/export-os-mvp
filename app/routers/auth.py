"""Authentication router.

MVP simplification:
- OTP is always '123456'.
- Token is a mock string returned to the client.

Production:
- Integrate real OTP provider.
- Use JWT + refresh.
- Add rate limiting.
"""

# Import uuid for token generation
import uuid

# Import FastAPI router
from fastapi import APIRouter, HTTPException

# Import schemas
from app.schemas import OTPRequest, OTPVerifyRequest, AuthTokenResponse

# Create router
router = APIRouter()


@router.post("/otp")
def request_otp(payload: OTPRequest) -> dict:
    """Start OTP login."""

    # In MVP, we do not actually send OTP
    return {"message": "OTP sent (mock). Use 123456 to verify.", "phone_number": payload.phone_number}


@router.post("/verify", response_model=AuthTokenResponse)
def verify_otp(payload: OTPVerifyRequest) -> AuthTokenResponse:
    """Verify OTP and return a mock auth token."""

    # Reject invalid OTP
    if payload.otp != "123456":
        raise HTTPException(status_code=401, detail="Invalid OTP")

    # Create mock token
    token = f"mock-{uuid.uuid4().hex}"

    # Return token
    return AuthTokenResponse(token=token)
