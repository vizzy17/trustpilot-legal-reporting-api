"""
SQLAlchemy ORM models for the Trustpilot Legal Reporting API.

Defines:
- User
- Business
- Review

These models map directly to database tables.
"""

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    reviewer_id = Column(String, primary_key=True)
    reviewer_name = Column(String, nullable=False)
    email_address = Column(String, nullable=False)
    reviewer_country = Column(String, nullable=False)

    # Relationship: one user → many reviews
    reviews = relationship("Review", back_populates="user")


class Business(Base):
    __tablename__ = "businesses"

    business_id = Column(String, primary_key=True)
    business_name = Column(String, nullable=False)

    # Relationship: one business → many reviews
    reviews = relationship("Review", back_populates="business")


class Review(Base):
    __tablename__ = "reviews"

    review_id = Column(String, primary_key=True)
    reviewer_id = Column(String, ForeignKey("users.reviewer_id"), nullable=False)
    business_id = Column(String, ForeignKey("businesses.business_id"), nullable=False)

    # Correct fields based on your dataset
    review_title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    review_date = Column(DateTime(timezone=True), nullable=False)
    review_ip_address = Column(String, nullable=False)

    # Relationships
    user = relationship("User", back_populates="reviews")
    business = relationship("Business", back_populates="reviews")
