import pdfplumber
import re
import json
import os

# --- CONFIGURATION ---
# INPUT_FOLDER = "../01_Input_Zone"
# JSON_FILE = "credit_map.json"


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

# Regex to find Course Codes (e.g., CST201 or AMT 302)
CODE_PATTERN = r"([A-Z]{3}\s?\d{3})"

def update_credit_map():
    print(f" Scanning '{INPUT_FOLDER}' for syllabus files...")
    
    if not os.path.exists(INPUT_FOLDER):
        print(" Error: Input Zone folder not found!")
        return

    # 1. Load existing map so we don't lose previous data
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            credit_map = json.load(f)
        print(f" Loaded existing database with {len(credit_map)} subjects.")
    else:
        credit_map = {}

    # 2. Find ALL files with 'syllabus' in the name
    syllabus_files = [f for f in os.listdir(INPUT_FOLDER) if "syllabus" in f.lower() and f.endswith(".pdf")]
    
    if not syllabus_files:
        print(" No files with 'syllabus' in the name found! (e.g., 'syllabus1.pdf')")
        return

    found_count = 0

    # 3. Loop through every syllabus file found
    for file_name in syllabus_files:
        file_path = os.path.join(INPUT_FOLDER, file_name)
        print(f" Processing: {file_name}...")

        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                
                for table in tables:
                    for row in table:
                        clean_row = [str(cell).strip() for cell in row if cell]
                        if not clean_row:
                            continue
                        
                        # Logic: Look for Code pattern in the row
                        row_text = " ".join(clean_row)
                        match = re.search(CODE_PATTERN, row_text)
                        
                        if match:
                            subject_code = match.group(1).replace(" ", "") 
                            
                            # Check last column for credit
                            last_col = clean_row[-1]
                            if last_col.isdigit():
                                credit = int(last_col)
                                if 0 <= credit <= 6:
                                    credit_map[subject_code] = credit
                                    found_count += 1

    # --- SAVE UPDATED MAP ---
    with open(JSON_FILE, "w") as f:
        json.dump(credit_map, f, indent=4)

    print(f"\n Success! Scanned {len(syllabus_files)} files.")
    print(f" Found/Updated {found_count} subjects.")
    print(f" Total Unique Subjects in Database: {len(credit_map)}")

if __name__ == "__main__":
    update_credit_map()