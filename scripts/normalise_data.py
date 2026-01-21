import sys
import os
import pandas as pd

# Ensure project root is on the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def normalise_reviews(engine):
    df = pd.read_sql("SELECT * FROM staging_reviews", engine)

    # Deduplicate
    df = df.drop_duplicates(
        subset=["review_id", "reviewer_id", "business_id", "review_date", "content"]
    )

    # USERS
    users = df[
        ["reviewer_id", "reviewer_name", "email_address", "reviewer_country"]
    ].drop_duplicates()

    # BUSINESSES
    businesses = df[
        ["business_id", "business_name"]
    ].drop_duplicates()

    # REVIEWS
    reviews = df[
        [
            "review_id",
            "reviewer_id",
            "business_id",
            "review_title",
            "content",
            "rating",
            "review_date",
            "review_ip_address",
        ]
    ]

    users.to_sql("users", engine, if_exists="append", index=False)
    businesses.to_sql("businesses", engine, if_exists="append", index=False)
    reviews.to_sql("reviews", engine, if_exists="append", index=False)

    print("Normalisation complete.")
