import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Load CSV
df = pd.read_csv("data/tp_reviews (1) (1) (1).csv")

# Write to Postgres
df.to_sql("reviews", engine, if_exists="replace", index=False)

print("Ingestion complete.")
