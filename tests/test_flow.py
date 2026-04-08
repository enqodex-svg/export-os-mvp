"""Integration-ish tests for the MVP flow.

These tests:
- Create a product
- Quote shipping
- Book shipment
- Generate documents
- Create payment link
- Track shipment

All mocked integrations are exercised.
"""

# Import FastAPI test client
from fastapi.testclient import TestClient

# Import app
from app.main import app

# Create client
client = TestClient(app)


def test_end_to_end_flow():
    """Verify end-to-end happy path."""

    # 1) Create product
    resp = client.post(
        "/products/",
        json={
            "name": "Handwoven Cushion Cover",
            "description": "Handwoven cotton cushion cover",
            "declared_value": 1200,
            "currency": "INR",
            "weight_kg": 1.2,
            "length_cm": 30,
            "width_cm": 20,
            "height_cm": 5,
        },
    )
    assert resp.status_code == 200
    product = resp.json()

    # 2) Readiness
    readiness = client.get(f"/products/{product['id']}/readiness").json()
    assert "score" in readiness

    # 3) Quote
    quote = client.post(
        "/shipping/quote",
        json={
            "destination": "UAE",
            "weight_kg": 1.2,
            "length_cm": 30,
            "width_cm": 20,
            "height_cm": 5,
            "incoterm": "DDU",
        },
    ).json()
    assert len(quote) > 0

    # 4) Book
    user_id = product["user_id"]

    book = client.post(
        "/shipping/book",
        json={
            "user_id": user_id,
            "product_id": product["id"],
            "destination_country": "UAE",
            "courier": quote[0]["courier"],
            "service_type": quote[0]["service_type"],
            "incoterm": quote[0]["incoterm"],
            "pickup_address": "Noida, Uttar Pradesh, India",
        },
    )
    assert book.status_code == 200
    shipment = book.json()

    # 5) Documents
    docs = client.post(f"/documents/{shipment['id']}/generate").json()
    assert len(docs) == 3

    # 6) Payment
    pay = client.post(
        "/payments/create-link",
        json={"shipment_id": shipment["id"], "amount_foreign": 200, "currency": "AED"},
    ).json()
    assert pay["status"] == "pending"

    # 7) Track
    tracking = client.get(f"/shipping/{shipment['id']}/track").json()
    assert "timeline" in tracking
