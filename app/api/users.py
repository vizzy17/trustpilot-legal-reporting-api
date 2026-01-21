from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import SessionLocal
from app.db.models import User, Review
from app.services.csv_export import generate_csv_response

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{reviewer_id}")
def get_user_account_info(reviewer_id: str, db: Session = Depends(get_db)):
    """
    Retrieve account information for a specific user.
    Returns results as a downloadable CSV file.
    """

    user = (
        db.query(
            User.reviewer_id,
            User.reviewer_name,
            User.email_address,
            User.reviewer_country,
        )
        .filter(User.reviewer_id == reviewer_id)
        .first()
    )

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    review_count = (
        db.query(func.count(Review.review_id))
        .filter(Review.reviewer_id == reviewer_id)
        .scalar()
    )

    rows = [
        (
            user.reviewer_id,
            user.reviewer_name,
            user.email_address,
            user.reviewer_country,
            review_count,
        )
    ]

    headers = [
        "reviewer_id",
        "reviewer_name",
        "email_address",
        "reviewer_country",
        "number_of_reviews",
    ]

    return generate_csv_response(
        rows=rows,
        headers=headers,
        filename=f"user_account_info_{reviewer_id}.csv",
    )
