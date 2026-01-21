import sys
import os
import pandas as pd
from sqlalchemy import Table, Column, String, Integer, MetaData, Date

# Ensure project root is on the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def ingest_raw_reviews(engine):
    metadata = MetaData()

    staging = Table(
        "staging_reviews",
        metadata,
        Column("review_id", String),
        Column("reviewer_id", String),
        Column("reviewer_name", String),
        Column("email_address", String),
        Column("reviewer_country", String),
        Column("business_id", String),
        Column("business_name", String),
        Column("business_category", String),
        Column("review_title", String),
        Column("content", String),
        Column("rating", Integer),
        Column("review_date", Date),
        Column("review_ip_address", String),
    )

    metadata.create_all(engine)

    # Load CSV
    df = pd.read_csv("data/trustpilot_reviews.csv")

    # Rename columns
    df = df.rename(columns={
        "Review Id": "review_id",
        "Reviewer Name": "reviewer_name",
        "Review Title": "review_title",
        "Review Rating": "rating",
        "Review Content": "content",
        "Review IP Address": "review_ip_address",
        "Business Id": "business_id",
        "Business Name": "business_name",
        "Reviewer Id": "reviewer_id",
        "Email Address": "email_address",
        "Reviewer Country": "reviewer_country",
        "Review Date": "review_date",
    })

    # Add missing column
    df["business_category"] = None

    # Convert Review Date safely
    df["review_date"] = pd.to_datetime(
        df["review_date"],
        errors="coerce",
        utc=True
    ).dt.tz_localize(None).dt.date

    # Write to staging table
    df.to_sql("staging_reviews", engine, if_exists="append", index=False)

    print("Staging ingestion complete.")
