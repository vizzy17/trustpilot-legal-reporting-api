"""
Database session and engine configuration.

This module is responsible for:
- Loading the DATABASE_URL from environment variables
- Creating the SQLAlchemy engine
- Creating a SessionLocal factory for request-scoped DB sessions

This design ensures:
- Local development uses .env (localhost)
- Docker uses environment variables (db hostname)
- No hardcoded credentials exist in the codebase
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from .env (Windows local development)
load_dotenv()

# Read the database connection string
DATABASE_URL = os.getenv("DATABASE_URL")

# Fail fast if the environment variable is missing
if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set. Create a .env file or pass it via environment variables."
    )

# Create the SQLAlchemy engine (manages DB connections)
engine = create_engine(DATABASE_URL)

# Create a session factory.
# autocommit=False and autoflush=False give explicit control over transactions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
