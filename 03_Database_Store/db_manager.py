import sqlite3
import json
import os
import pandas as pd

# --- CONFIGURATION ---
JSON_SOURCE = "../02_Extraction_Engine/raw_data.json"
DB_FILE = "results.db"

def init_db():
    """Creates the empty database table if it doesn't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create the RESULT table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            register_id TEXT,
            subject_code TEXT,
            grade TEXT,
            credits INTEGER DEFAULT 0,
            points INTEGER DEFAULT 0
        )
    ''')
    
    conn.commit()
    conn.close()
    print(" Database initialized (Table 'results' created).")

def load_data():
    """Reads the JSON file and inserts it into the Database."""
    if not os.path.exists(JSON_SOURCE):
        print(f"Error: {JSON_SOURCE} not found. Run extractor first!")
        return

    # 1. Load JSON
    with open(JSON_SOURCE, "r") as f:
        data = json.load(f)
    
    print(f" Loaded {len(data)} records from JSON.")

    # 2. Connect to DB
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # 3. Clear old data (Optional: for fresh start)
    cursor.execute("DELETE FROM results")
    
    # 4. Insert new data
    # We use 'executemany' which is very fast
    # We create a list of tuples: (RegID, Subject, Grade)
    to_insert = [(d['Register_ID'], d['Subject_Code'], d['Grade']) for d in data]
    
    cursor.executemany('''
        INSERT INTO results (register_id, subject_code, grade) 
        VALUES (?, ?, ?)
    ''', to_insert)

    conn.commit()
    conn.close()
    print(f" Success! Inserted {len(to_insert)} rows into SQLite Database.")

def view_data():
    """Helper to verify data using Pandas"""
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql("SELECT * FROM results LIMIT 10", conn)
    print("\n Database Preview:")
    print(df)
    conn.close()

if __name__ == "__main__":
    init_db()
    load_data()
    view_data()