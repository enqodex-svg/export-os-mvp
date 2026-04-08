"""Database configuration.

- Uses DATABASE_URL if provided (e.g., Postgres in Docker).
- Falls back to local SQLite for quick local development.

SECURITY NOTE:
- Never hardcode production credentials.
- Use environment variables or secret managers.
"""

# Import os for reading environment variables
import os

# Default SQLite DB for local dev
DEFAULT_SQLITE_URL = "sqlite:///./exportos.sqlite"

# Read DATABASE_URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_SQLITE_URL)
