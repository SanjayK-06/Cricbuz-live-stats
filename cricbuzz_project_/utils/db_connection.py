import psycopg2
import pandas as pd
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

# ---------------- Load ENV ----------------
dotenv_path = r"C:\Users\Amirtha\Downloads\cricbuzz_project_sanjay\utils\.env"
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# 🔑 Database connection values from .env
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "Cricbuz")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "susmitha2102")

# 🔑 Custom defaults from .env
DEFAULT_RUNS = int(os.getenv("DEFAULT_RUNS", "0"))
DEFAULT_AVG = float(os.getenv("DEFAULT_AVG", "0.0"))

def get_conn():
    """Return PostgreSQL connection"""
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def execute_query(query, params=None):
    """Run SELECT queries and return DataFrame"""
    try:
        conn = get_conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, params or ())
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return pd.DataFrame(rows)
    except Exception as e:
        print(f"❌ Error executing query: {e}")
        return None

def execute_update(query, params=None):
    """Run INSERT, UPDATE, DELETE queries"""
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(query, params or ())
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error executing update: {e}")
        return False

