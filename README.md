Trustpilot Legal Reporting API — Take‑Home Solution
A lightweight, production‑style FastAPI service that ingests a mock Trustpilot reviews dataset, normalises it into a relational PostgreSQL schema, and exposes CSV‑exporting API endpoints to support ad‑hoc legal and compliance data requests.

The API answers the three core legal queries:

Provide reviews for business X

Provide reviews by user Y

Provide user account information for user Z

In addition, the solution includes optional enhancements such as filtering, pagination, operational endpoints, and a /businesses endpoint with CSV export.

1. Overview
This project demonstrates:

A clean ETL pipeline (CSV → staging → normalised tables)

A modular FastAPI application

CSV export for legal/compliance workflows

Clear separation between required and enhancement endpoints

Senior‑level engineering practices: structure, clarity, observability, and documentation

The solution is intentionally lightweight to fit the 3–6 hour assessment window while still showing production‑minded thinking.

2. Repository Structure
Code
trustpilot-legal-reporting-api/
│
├── app/
│   ├── api/
│   │   ├── reviews.py
│   │   ├── users.py
│   │   ├── businesses.py
│   │   └── system.py
│   ├── db/
│   │   ├── models.py
│   │   ├── session.py
│   │   └── __init__.py
│   ├── services/
│   │   └── csv_export.py
│   └── main.py
│
├── scripts/
│   ├── setup_db.py
│   ├── ingest_reviews.py
│   └── normalise_data.py
│
├── data/
│   └── trustpilot_reviews.csv
│
├── requirements.txt
└── README.md
3. Architecture Diagram (Lightweight)
Code
Client (Legal Team / Tools)
        |
        v
   FastAPI App
        |
        v
 Normalised PostgreSQL DB
        ^
        |
 ETL Scripts (staging → clean)
        ^
        |
   trustpilot_reviews.csv
4. Data Lineage (Governance‑Style)
Code
CSV → staging_reviews → cleaned_reviews → {users, businesses, reviews} → API → Legal Team
5. Entity Relationship Diagram (ERD)
Code
USERS (reviewer_id PK) 1 ──── * REVIEWS * ──── 1 BUSINESSES (business_id PK)
6. Setup Instructions
1. Create virtual environment
Code
python -m venv .venv
.venv\Scripts\activate
2. Install dependencies
Code
pip install -r requirements.txt
3. Configure environment
Create .env:

Code
DATABASE_URL=postgresql://postgres:password@localhost:5432/trustpilot
4. Run ETL
Code
python -m scripts.setup_db
This:

Creates tables

Loads raw CSV into staging

Normalises into users, businesses, reviews

7. Running the API
Start the server:

Code
uvicorn app.main:app --reload
Open Swagger:

Code
http://127.0.0.1:8000/docs
8. API Endpoints
Required (Assessment Spec)
GET /reviews/business/{business_id}
Returns all reviews for a business as CSV.

GET /reviews/user/{reviewer_id}
Returns all reviews written by a user as CSV.

GET /users/{reviewer_id}
Returns user account information.

Enhancements (Optional)
GET /reviews/
Filtering + pagination + CSV export
Supports:

start_date / end_date

min_rating / max_rating

country

limit / offset

GET /businesses/
Returns all businesses (JSON).

GET /businesses/export
Returns all businesses as CSV (enhancement).

GET /health
Heartbeat.

GET /stats
Returns table counts:

staging_reviews

users

businesses

reviews

9. Example Queries
Reviews for a business
Code
/reviews/business/24a6a92a-f745-455f-b669-f2f02842039f
Reviews by a user
Code
/reviews/user/8f3c1d2e-9b4a-4c1a-8e2f-1c2d3e4f5a6b
Filtered review export
Code
/reviews?min_rating=4&country=uk&start_date=2024-01-01&limit=100
Export businesses as CSV
Code
/businesses/export
10. Data Cleaning & Normalisation
Ingestion
Raw CSV → staging table

Deduplication
Rules applied:

Duplicate review_id

Same reviewer + business + date + content

Normalisation
Distinct reviewers → users

Distinct businesses → businesses

Cleaned reviews → reviews

Governance
PK/FK constraints

Referential integrity

Indexes on:

reviewer_id

business_id

review_date

11. Performance Considerations
Indexes added on high‑cardinality join/filter fields

CSV streaming avoids loading large datasets into memory

Pagination prevents large result sets

Filtering pushed down to SQL for efficiency

Normalised schema reduces duplication and improves query speed

Avoided ORM overhead for bulk operations (raw SQL used where appropriate)

12. Productionisation Considerations
If this were promoted beyond PoC:

Add Docker Compose (API + Postgres)

Add authentication / API keys

Add async SQLAlchemy for concurrency

Add caching for repeated legal queries

Add CI/CD pipeline

Add S3 export for large CSVs

Add monitoring (Prometheus + Grafana)

13. How AI Was Used
AI was used to:

Accelerate boilerplate FastAPI scaffolding

Draft initial documentation

Suggest schema normalisation patterns

Assist with CSV export logic

Provide debugging hints during ETL development

All final code, validation, and architectural decisions were made manually.

14. Testing
Manual Smoke Tests (via Swagger)
GET /reviews/business/{id}

GET /reviews/user/{id}

GET /users/{id}

GET /reviews

GET /businesses

GET /businesses/export

Automated Tests (Future Work)
pytest suite for:

ETL correctness

API response structure

CSV export validation

15. Conclusion
This solution delivers a clean, modular, and production‑minded PoC that satisfies the assessment requirements while demonstrating:

Strong engineering fundamentals

Clear documentation

Thoughtful design choices

Extendability

Operational awareness