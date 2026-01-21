"""
CSV ingestion script for Trustpilot Legal Reporting API.

This script:
- Creates database tables if they don't exist
- Reads a CSV file containing review data
- Normalises column types (dates, integers)
- Upserts Users and Businesses
- Inserts or updates Reviews
- Can be run from the command line using:
      python -m app.db.ingest data/reviews.csv
"""

import sys
import os
import pandas as pd
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import engine, SessionLocal
from app.db.models import Base, User, Business, Review


def create_tables():
    """
    Create all database tables defined in SQLAlchemy models.

    Safe to call multiple times because SQLAlchemy checks for existence.
    """
    Base.metadata.create_all(bind=engine)


def ingest_reviews(csv_path: str):
    """
    Ingest a CSV file into the database.

    Expected CSV columns:
    - Reviewer Id
    - Reviewer Name
    - Email Address
    - Reviewer Country
    - Business Id
    - Business Name
    - Review Id
    - Review Title
    - Review Content
    - Review Rating
    - Review Date
    - Review IP Address
    """

    # Ensure the CSV file exists
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    # Load CSV into a DataFrame
    df = pd.read_csv(csv_path)

    # Normalise column names (remove trailing spaces)
    df.columns = [col.strip() for col in df.columns]

    # Convert date and rating fields to correct types
    df["Review Date"] = pd.to_datetime(df["Review Date"], utc=True)
    df["Review Rating"] = df["Review Rating"].astype(int)

    # Create a database session
    session: Session = SessionLocal()

    try:
        for _, row in df.iterrows():

            # Upsert User record
            user = User(
                reviewer_id=row["Reviewer Id"],
                reviewer_name=row["Reviewer Name"],
                email_address=row["Email Address"],
                reviewer_country=row["Reviewer Country"],
            )
            session.merge(user)

            # Upsert Business record
            business = Business(
                business_id=row["Business Id"],
                business_name=row["Business Name"],
            )
            session.merge(business)

            # Insert or update Review record
            review = Review(
                review_id=row["Review Id"],
                reviewer_id=row["Reviewer Id"],
                business_id=row["Business Id"],
                review_title=row["Review Title"],
                review_content=row["Review Content"],
                review_rating=row["Review Rating"],
                review_date=row["Review Date"],
                review_ip_address=row["Review IP Address"],
            )
            session.merge(review)

        # Commit all changes after processing the file
        session.commit()
        print(f"Ingestion complete. Rows processed: {len(df)}")

    except Exception as exc:
        # Roll back the transaction on any error
        session.rollback()
        print(f"Error during ingestion: {exc}")
        raise

    finally:
        # Always close the session
        session.close()


if __name__ == "__main__":
    """
    Command-line entry point.

    Ensures the script is run with exactly one argument (CSV path).
    """
    if len(sys.argv) != 2:
        print("Usage: python -m app.db.ingest <path_to_csv>")
        sys.exit(1)

    csv_file = sys.argv[1]

    create_tables()
    ingest_reviews(csv_file)
