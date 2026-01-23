📘 Trustpilot Legal Reporting API — Take‑Home Solution
A lightweight, production‑style FastAPI service that ingests a mock Trustpilot reviews dataset, normalises it into a relational schema, and exposes CSV‑exporting API endpoints to support ad‑hoc legal and compliance data requests.

The API answers the three core legal queries:

Provide reviews for business X

Provide reviews by user Y

Provide user account information for user Z

In addition, the solution includes enhancements such as filtering, pagination, operational endpoints, and a /businesses endpoint with CSV export.

🧭 Overview
This project demonstrates:

A clean ETL pipeline (CSV → staging → normalised tables)

A modular FastAPI application

CSV export for legal/compliance workflows

Clear separation between required and enhancement endpoints

Senior‑level engineering practices: structure, clarity, observability, documentation

A lightweight design showing production‑minded thinking



📂 Repository Structure
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


🏗️ Architecture Diagram (Lightweight)
Code
Client (Legal Team / Tools)
            |
            v
        FastAPI App
            |
            v
 Normalised SQLite DB (Codespaces)
            ^
            |
 ETL Scripts (staging → clean)
            ^
            |
   trustpilot_reviews.csv


🔄 Data Lineage (Governance‑Style)
Code
CSV
  → staging_reviews
      → cleaned_reviews
          → {users, businesses, reviews}
              → API
                  → Legal Team


🧬 Entity Relationship Diagram (ERD)
Code
USERS (reviewer_id PK)
        1 ───── * REVIEWS * ───── 1
BUSINESSES (business_id PK)


🚀 Running the Project (GitHub Codespaces — Recommended)
This project is fully runnable inside GitHub Codespaces, which provides a clean, reproducible environment with no local setup required.

1. Create and activate a virtual environment
bash
python -m venv .venv
source .venv/bin/activate
2. Install dependencies
bash
pip install -r requirements.txt
3. Configure environment (.env)
Codespaces does not support PostgreSQL without elevated permissions, so this project uses SQLite for a frictionless, portable setup.

bash
echo DATABASE_URL=sqlite:///./trustpilot.db > .env
4. Run the ETL pipeline
bash
python -m scripts.setup_db
This:

Creates tables

Loads raw CSV into staging

Normalises into users, businesses, reviews

5. Start the API
bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
6. Open the public Swagger UI
In Codespaces:

Open the PORTS tab

Locate port 8000

Click the forwarded URL

Append /docs

Example:

Code
https://vigilant-bassoon-7wv6w45vj5vcxv65-8000.app.github.dev/docs
🌍 Live Demo (Public URL)
A live version of the API is available here:

Code
https://vigilant-bassoon-7wv6w45vj5vcxv65-8000.app.github.dev/docs
This allows the reviewer to explore all endpoints directly in Swagger.



🧪 Local Development (Optional)
If running locally with PostgreSQL:

bash
DATABASE_URL=postgresql://postgres:password@localhost:5432/trustpilot
python -m scripts.setup_db
uvicorn app.main:app --reload
📡 API Endpoints
Required (Assessment Spec)
GET /reviews/business/{business_id}
Returns all reviews for a business as CSV.

GET /reviews/user/{reviewer_id}
Returns all reviews written by a user as CSV.

GET /users/{reviewer_id}
Returns user account information.

Enhancements (Optional)
GET /reviews/
Filtering + pagination + CSV export.
Supports:

start_date / end_date

min_rating / max_rating

country

limit / offset

GET /businesses/
Returns all businesses (JSON).

GET /businesses/export
Returns all businesses as CSV.

GET /health
Heartbeat.

GET /stats
Returns table counts:

staging_reviews

users

businesses

reviews



📝 Example Queries
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


🧹 Data Cleaning & Normalisation
Ingestion
Raw CSV → staging table

Deduplication Rules
Duplicate review_id

Same reviewer + business + date + content

Normalisation
Distinct reviewers → users

Distinct businesses → businesses

Cleaned reviews → reviews

Governance
PK/FK constraints

Referential integrity

Indexes on reviewer_id, business_id, review_date


⚡ Performance Considerations
Indexes on high‑cardinality join/filter fields

CSV streaming avoids loading large datasets into memory

Pagination prevents large result sets

Filtering pushed down to SQL for efficiency

Normalised schema reduces duplication

Avoided ORM overhead for bulk operations



🏭 Productionisation Considerations
If promoted beyond PoC:

Docker Compose (API + Postgres)

Authentication / API keys

Async SQLAlchemy

Caching for repeated legal queries

CI/CD pipeline

S3 export for large CSVs

Monitoring (Prometheus + Grafana)



🤖 How AI Was Used
AI was used to:

Accelerate boilerplate FastAPI scaffolding

Draft initial documentation

Suggest schema normalisation patterns

Assist with CSV export logic

Provide debugging hints during ETL development

All final code, validation, and architectural decisions were made manually.



🧪 Testing
Manual Smoke Tests (via Swagger)

GET /reviews/business/{id}

GET /reviews/user/{id}

GET /users/{id}

GET /reviews

GET /businesses

GET /businesses/export



Automated Tests (Future Work)
ETL correctness

API response structure

CSV export validation

🚀 Deployment
The API is deployed on Render and publicly accessible without authentication.

Public Swagger UI:  
[https://trustpilot-legal-reporting-api.onrender.com/docs]

This deployment uses:

Render Web Service (Free tier)

Uvicorn as the ASGI server

SQLite as the PoC database

FastAPI auto‑generated OpenAPI docs for interactive testing

The service is started using:

Code
uvicorn app.main:app --host 0.0.0.0 --port 10000
A render.yaml file is included in the repository to support reproducible deployments.


🏁 Conclusion
This solution delivers a clean, modular, and production‑minded PoC that satisfies the assessment requirements while demonstrating:

Strong engineering fundamentals

Clear documentation

Thoughtful design choices

Extendability

Operational awareness
