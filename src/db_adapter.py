"""
Database Adapter - Switches between SQLite and PostgreSQL based on environment
"""
import os

# Check if we're running on Vercel or have a DATABASE_URL configured
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL and not DATABASE_URL.startswith("sqlite"):
    # Use PostgreSQL for Vercel/production
    from src.db_postgres import get_db, init_db, RoseGlassDB
else:
    # Use SQLite for local development
    from src.db import get_db, init_db, RoseGlassDB

# Export the functions so they can be imported from this module
__all__ = ['get_db', 'init_db', 'RoseGlassDB']
