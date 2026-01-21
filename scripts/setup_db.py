import sys
import os

# Ensure project root is on the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.ingest_reviews import ingest_raw_reviews
from scripts.normalise_data import normalise_reviews
from app.db.session import engine
from app.db.models import Base


def main():
    print("Creating tables...")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    print("Ingesting raw CSV into staging...")
    ingest_raw_reviews(engine)

    print("Normalising data...")
    normalise_reviews(engine)

    print("Database setup complete.")


if __name__ == "__main__":
    main()
