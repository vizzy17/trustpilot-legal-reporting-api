"""
Reviews API Router

Provides:
1. Required endpoints:
   - GET /reviews/business/{business_id}
   - GET /reviews/user/{reviewer_id}

2. Advanced reporting endpoint:
   - GET /reviews/ (filtering + pagination + CSV)

All endpoints return CSV files suitable for legal/compliance reporting.
"""

from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, cast, DateTime

from app.db.session import SessionLocal
from app.db.models import Review, User
from app.services.csv_export import generate_csv_response

router = APIRouter()


# ---------------------------------------------------------------------------
# Database session dependency
# ---------------------------------------------------------------------------
def get_db():
    """Provide a scoped SQLAlchemy session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Utility: Safe date parsing
# ---------------------------------------------------------------------------
def parse_date(value: Optional[str]) -> Optional[datetime]:
    """Convert YYYY-MM-DD string to datetime, raising 400 on invalid format."""
    if value is None:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid date format '{value}'. Expected YYYY-MM-DD."
        )


# ---------------------------------------------------------------------------
# 1. ORIGINAL TASK ENDPOINT: Get reviews for a business
# ---------------------------------------------------------------------------
@router.get("/business/{business_id}", tags=["Required"])
def get_reviews_for_business(business_id: str, db: Session = Depends(get_db)):
    """
    Retrieve all reviews for a specific business.
    Returns results as a downloadable CSV file.
    """

    reviews = (
        db.query(
            Review.review_id,
            Review.reviewer_id,
            Review.business_id,
            Review.review_title,
            Review.content,
            Review.rating,
            Review.review_date,
            Review.review_ip_address,
        )
        .filter(Review.business_id == business_id)
        .order_by(Review.review_date.desc())
        .all()
    )

    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found for this business")

    rows = [
        (
            r.review_id,
            r.reviewer_id,
            r.business_id,
            r.review_title,
            r.content,
            r.rating,
            r.review_date,
            r.review_ip_address,
        )
        for r in reviews
    ]

    headers = [
        "review_id",
        "reviewer_id",
        "business_id",
        "review_title",
        "content",
        "rating",
        "review_date",
        "review_ip_address",
    ]

    return generate_csv_response(
        rows=rows,
        headers=headers,
        filename=f"reviews_business_{business_id}.csv",
    )


# ---------------------------------------------------------------------------
# 2. ORIGINAL TASK ENDPOINT: Get reviews by user
# ---------------------------------------------------------------------------
@router.get("/user/{reviewer_id}", tags=["Required"])
def get_reviews_by_user(reviewer_id: str, db: Session = Depends(get_db)):
    """
    Retrieve all reviews written by a specific user.
    Returns results as a downloadable CSV file.
    """

    reviews = (
        db.query(
            Review.review_id,
            Review.reviewer_id,
            Review.business_id,
            Review.review_title,
            Review.content,
            Review.rating,
            Review.review_date,
            Review.review_ip_address,
        )
        .filter(Review.reviewer_id == reviewer_id)
        .order_by(Review.review_date.desc())
        .all()
    )

    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found for this user")

    rows = [
        (
            r.review_id,
            r.reviewer_id,
            r.business_id,
            r.review_title,
            r.content,
            r.rating,
            r.review_date,
            r.review_ip_address,
        )
        for r in reviews
    ]

    headers = [
        "review_id",
        "reviewer_id",
        "business_id",
        "review_title",
        "content",
        "rating",
        "review_date",
        "review_ip_address",
    ]

    return generate_csv_response(
        rows=rows,
        headers=headers,
        filename=f"reviews_user_{reviewer_id}.csv",
    )


# ---------------------------------------------------------------------------
# 3. ADVANCED ENDPOINT: Filtering + pagination
# ---------------------------------------------------------------------------
@router.get("/", tags=["Enhancements"])
def list_reviews(
    db: Session = Depends(get_db),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    min_rating: Optional[int] = Query(None, ge=1, le=5),
    max_rating: Optional[int] = Query(None, ge=1, le=5),
    country: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    """
    Advanced reporting endpoint:
    - Filter by date range, rating range, country
    - Paginate results
    - Export CSV
    """

    start_dt = parse_date(start_date)
    end_dt = parse_date(end_date)

    filters = []

    # Date filtering (DB column is now TIMESTAMP)
    if start_dt:
        filters.append(Review.review_date >= start_dt)
    if end_dt:
        filters.append(Review.review_date <= end_dt)

    # Rating filtering
    if min_rating is not None:
        filters.append(Review.rating >= min_rating)
    if max_rating is not None:
        filters.append(Review.rating <= max_rating)

    # Base query
    query = db.query(
        Review.review_id,
        Review.reviewer_id,
        Review.business_id,
        Review.review_title,
        Review.content,
        Review.rating,
        Review.review_date,
        Review.review_ip_address,
    )

    # Country filtering (corrected)
    if country:
        query = query.join(User, User.reviewer_id == Review.reviewer_id)
        filters.append(func.lower(User.reviewer_country) == country.lower())

    # Apply filters
    if filters:
        query = query.filter(and_(*filters))

    # Count before pagination
    total_count = query.count()

    # Apply pagination
    results = (
        query.order_by(Review.review_date.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    rows = [
        (
            r.review_id,
            r.reviewer_id,
            r.business_id,
            r.review_title,
            r.content,
            r.rating,
            r.review_date,
            r.review_ip_address,
        )
        for r in results
    ]

    headers = [
        "review_id",
        "reviewer_id",
        "business_id",
        "review_title",
        "content",
        "rating",
        "review_date",
        "review_ip_address",
    ]

    response = generate_csv_response(
        rows=rows,
        headers=headers,
        filename=f"reviews_limit{limit}_offset{offset}.csv",
    )

    response.headers["X-Total-Count"] = str(total_count)
    response.headers["X-Limit"] = str(limit)
    response.headers["X-Offset"] = str(offset)

    return response
