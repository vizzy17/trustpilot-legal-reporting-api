from fastapi import APIRouter
from sqlalchemy import text
from app.db.session import engine

router = APIRouter()

@router.get("/health", tags=["Enhancements"])
def health_check():
    return {"status": "ok"}

@router.get("/stats", tags=["Enhancements"])
def stats():
    with engine.connect() as conn:
        return {
            "staging_reviews": conn.execute(text("SELECT COUNT(*) FROM staging_reviews")).scalar(),
            "users": conn.execute(text("SELECT COUNT(*) FROM users")).scalar(),
            "businesses": conn.execute(text("SELECT COUNT(*) FROM businesses")).scalar(),
            "reviews": conn.execute(text("SELECT COUNT(*) FROM reviews")).scalar(),
        }
