import sqlite3
import json
import os

# --- CONFIGURATION ---
# DB_PATH = "../03_Database_Store/results.db"
# CREDIT_MAP_FILE = "credit_map.json"

import os

# --- ABSOLUTE PATH CALCULATION ---
# 1. Get the exact folder where this calculator script lives (e.g., .../04_Calculation_Core)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Go up one level to the main project root folder (.../KTU-Result-Analyzer)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

# 3. Define the unbreakable absolute paths
DB_PATH = os.path.join(ROOT_DIR, "03_Database_Store", "results.db")

# Since credit_map.json is in the exact same folder as this script, we use CURRENT_DIR
CREDIT_MAP_FILE = os.path.join(CURRENT_DIR, "credit_map.json")

# --- GRADE POINTS (KTU 2019 Scheme) ---
# Adjust these values if your scheme is different
GRADE_VALUES = {
    "S": 10,
    "A+": 9,
    "A": 8.5,
    "B+": 8,
    "B": 7.5,
    "C+": 7,
    "C": 6.5,
    "D": 6,
    "P": 5.5,
    "F": 0,
    "FE": 0,
    "I": 0,
    "Absent": 0
}

def load_credit_map():
    if not os.path.exists(CREDIT_MAP_FILE):
        print(" Error: credit_map.json not found!")
        return {}
    with open(CREDIT_MAP_FILE, "r") as f:
        return json.load(f)

def calculate_scores():
    print(" Starting Calculation Engine...")
    
    credit_map = load_credit_map()
    # Note: We continue even if map is empty, because we have guessing logic now.

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, subject_code, grade FROM results")
    rows = cursor.fetchall()
    
    updated_count = 0

    print(f" Processing {len(rows)} records...")

    for row in rows:
        row_id, subject, grade = row
        clean_grade = grade.strip()
        grade_point = GRADE_VALUES.get(clean_grade, 0)
        
        # --- SMART CREDIT LOGIC ---
        if subject in credit_map:
            # 1. Exact Match found in JSON
            subject_credit = credit_map[subject]
        else:
            # 2. Not found? Try to GUESS.
            # Most Theory courses (T) are 4 credits.
            # Most Lab courses (L) are 2 credits.
            if 'L' in subject and not subject.startswith('PHL'): 
                # e.g., CSL201, MEL203
                subject_credit = 2
                print(f"⚠️ Guessed 2 credits for unknown Lab: {subject}")
            elif 'MCN' in subject or 'HUT' in subject:
                 # Constitution/Life Skills usually 0 or pass/fail in result calculation often
                subject_credit = 0
            else:
                # Default for unknown Theory subject
                subject_credit = 4
                print(f" Guessed 4 credits for unknown Subject: {subject}")

        # Calculate Total Points
        total_points = grade_point * subject_credit

        cursor.execute('''
            UPDATE results 
            SET credits = ?, points = ? 
            WHERE id = ?
        ''', (subject_credit, total_points, row_id))
        
        updated_count += 1

    conn.commit()
    conn.close()
    print(f" Success! Updated scores for {updated_count} records.")
    
    credit_map = load_credit_map()
    if not credit_map:
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Fetch all rows
    cursor.execute("SELECT id, subject_code, grade FROM results")
    rows = cursor.fetchall()
    
    updated_count = 0

    print(f" Processing {len(rows)} records...")

    for row in rows:
        row_id, subject, grade = row
        
        # A. Find Points for Grade (e.g., 'A+' -> 9)
        # Use .strip() to remove accidental spaces
        clean_grade = grade.strip()
        grade_point = GRADE_VALUES.get(clean_grade, 0)
        
        # B. Find Credits for Subject (e.g., 'CST202' -> 4)
        subject_credit = credit_map.get(subject, 0) # Default to 0 if not in map

        # C. Calculate Total Points (Credit * Grade Point)
        total_points = grade_point * subject_credit

        # D. Update Database
        cursor.execute('''
            UPDATE results 
            SET credits = ?, points = ? 
            WHERE id = ?
        ''', (subject_credit, total_points, row_id))
        
        updated_count += 1

    conn.commit()
    conn.close()
    print(f" Success! Updated scores for {updated_count} records.")

def verify_data():
    """Show a few rows to prove it worked"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Fetch rows where points > 0 to see if it worked
    cursor.execute("SELECT * FROM results WHERE points > 0 LIMIT 5")
    rows = cursor.fetchall()
    print("\n Verification (Non-Zero Rows):")
    print("ID | RegID | Sub | Grade | Credit | Points")
    for r in rows:
        print(r)
    conn.close()

if __name__ == "__main__":
    calculate_scores()
    verify_data()