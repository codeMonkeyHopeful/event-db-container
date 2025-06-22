import os
import psycopg2
from faker import Faker
from time import sleep

# Wait a bit to ensure DB is ready
print("Waiting for DB...")
sleep(5)

# Connect to DB
conn = psycopg2.connect(
    host=os.environ.get("DB_HOST", "localhost"),
    database=os.environ["DB_NAME"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASS"],
    port=os.environ.get("DB_PORT", 5432)
)

cur = conn.cursor()

# Create table
cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        bio TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""")

# Generate 50 fake users
faker = Faker()
users = [(faker.name(), faker.unique.email(), faker.sentence()) for _ in range(50)]

# Insert users
args_str = ",".join(cur.mogrify("(%s, %s, %s)", u).decode("utf-8") for u in users)
cur.execute(f"INSERT INTO users (name, email, bio) VALUES {args_str} ON CONFLICT (email) DO NOTHING;")

conn.commit()
cur.close()
conn.close()
print("Database seeded with 50 fake users.")
