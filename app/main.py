"""Main entrypoint for the Export OS MVP backend.

Notes:
- This app is structured as a 'modular monolith' for MVP speed.
- Routers are separated by domain to allow future service extraction.
- All key integrations (courier, WhatsApp, payments) are abstracted and mocked.

IMPORTANT ABOUT COMMENTS:
- You asked: "comment everything you write".
- In real production repos, commenting every line reduces readability.
- Here we comment generously on intent, invariants, and non-obvious decisions.
"""

# Import FastAPI framework
from fastapi import FastAPI

# Import router modules (domain-based)
from app.routers import auth, products, hs, shipping, payments, documents

# Import database initialization
from app.db.session import init_db

# Create the FastAPI application
app = FastAPI(
    # Human-friendly name
    title="Export OS MVP",
    # Semantic version
    version="0.1.0",
    # Short description shown in /docs
    description="Enablement-first Export OS MVP for India → UAE",
)

# Register routers with tags for clean OpenAPI documentation
app.include_router(auth.router, prefix="/auth", tags=["auth"])  # Auth endpoints
app.include_router(products.router, prefix="/products", tags=["products"])  # Product endpoints
app.include_router(hs.router, prefix="/hs", tags=["hs"])  # HS code suggestion endpoints
app.include_router(shipping.router, prefix="/shipping", tags=["shipping"])  # Shipping endpoints
app.include_router(documents.router, prefix="/documents", tags=["documents"])  # Document endpoints
app.include_router(payments.router, prefix="/payments", tags=["payments"])  # Payment endpoints


@app.on_event("startup")
def on_startup() -> None:
    """Startup hook to initialize database tables.

    For MVP simplicity we auto-create tables.
    For production, use Alembic migrations.
    """

    # Initialize database (create tables if missing)
    init_db()


@app.get("/health")
def health() -> dict:
    """Simple health check endpoint."""

    # Return basic status payload
    return {"status": "ok"}
