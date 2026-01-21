"""
Main entry point for the FastAPI application.

Responsibilities:
- Create the FastAPI app instance
- Register API routers
- Provide a clean, minimal startup surface
"""

from fastapi import FastAPI

# Import API routers
from app.api.reviews import router as reviews_router
from app.api.users import router as users_router
from app.api.system import router as system_router   # NEW (health + stats)
from app.api.businesses import router as businesses_router  # if you have it

# Create the FastAPI application instance
app = FastAPI(
    title="Trustpilot Legal Reporting API",
    description="PoC API to support ad-hoc legal data requests",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Required",
            "description": "Endpoints required by the assessment"
        },
        {
            "name": "Enhancements",
            "description": "Optional improvements for observability and reporting"
        }
    ]
)

# Register API routers
app.include_router(reviews_router, prefix="/reviews")
app.include_router(users_router, prefix="/users")
app.include_router(system_router)  # /health, /stats
app.include_router(businesses_router, prefix="/businesses")  # optional

