# app/rag/config.py
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCHEMA_DB_PATH = os.path.join(BASE_DIR, "schema_db")
