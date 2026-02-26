import os
import sqlite3
import pdfplumber
import re

# --- CONFIGURATION ---
INPUT_PDF = os.path.join(os.path.dirname(__file__), '..', '01_Input_Zone', 'sample_result.pdf')
DB_PATH = os.path.join(os.path.dirname(__file__), '..', '03_Database_Store', 'results.db')

def setup_database():
    """Creates the SQLite table with the batch_year column."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
            register_id TEXT,
            subject_code TEXT,
            grade TEXT,
            batch_year INTEGER,
            credits INTEGER DEFAULT 0,
            points INTEGER DEFAULT 0,
            PRIMARY KEY (register_id, subject_code)
        )
    ''')
    conn.commit()
    return conn

def extract_deterministically():
    print("⚙️ Starting Deterministic Fast-Extraction Pipeline...")
    conn = setup_database()
    cursor = conn.cursor()

    try:
        full_text = ""
        with pdfplumber.open(INPUT_PDF) as pdf:
            total_pages = len(pdf.pages)
            print(f"📄 Found PDF with {total_pages} pages. Reading text into memory...")
            
            # 1. Read the entire document into one giant string
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + " "
        
        # 2. Normalize Text (The "Cleaner")
        # KTU PDFs often break a single line in half. By removing newlines,
        # we stitch broken grades (like "CST463 \n (P)") back together.
        full_text = full_text.replace('\n', ' ')
        
        # 3. The "State Machine" Splitter
        # We slice the giant string into chunks every time we see a Register ID.
        # Pattern matches IDs like CEK22CS061 or LCEK21CS060
        id_pattern = r'([A-Z]{2,4}\d{2}[A-Z]{2}\d{3})'
        parts = re.split(id_pattern, full_text)
        
        inserted_count = 0
        student_count = 0
        
        print("🔍 Harvesting subjects and grades...")
        
        # The split array looks like: [junk, ID1, grades1, ID2, grades2, ...]
        # We step through the array grabbing the ID and its corresponding grade chunk.
        for i in range(1, len(parts) - 1, 2):
            register_id = parts[i].strip()
            grades_chunk = parts[i+1]
            
            # Extract Batch Year (e.g., "22" from "CEK22CS061")
            year_match = re.search(r'\d{2}', register_id)
            batch_year = int(year_match.group()) if year_match else 0
            
            # 4. The Regex Harvester
            # Finds every instance of "3 Letters + 3 Numbers + (Grade)" inside the chunk
            # e.g., CST401(B+) or MCN401 (Absent)
            subject_pattern = r'([A-Z]{3}\d{3})\s*\(([^)]+)\)'
            subjects_found = re.findall(subject_pattern, grades_chunk)
            
            if subjects_found:
                student_count += 1
                for sub_code, grade in subjects_found:
                    sub_code = sub_code.strip()
                    grade = grade.strip()
                    
                    try:
                        # Insert into database, ignoring duplicates
                        cursor.execute('''
                            INSERT OR IGNORE INTO results 
                            (register_id, subject_code, grade, batch_year)
                            VALUES (?, ?, ?, ?)
                        ''', (register_id, sub_code, grade, batch_year))
                        
                        if cursor.rowcount > 0:
                            inserted_count += 1
                    except Exception as e:
                        pass # Ignore SQLite duplicate warnings silently
        
        conn.commit()
        print(f"✅ Successfully processed {student_count} students.")
        print(f"✅ Saved {inserted_count} total grade records to database.")

    except FileNotFoundError:
        print(f"❌ Error: Could not find PDF file at {INPUT_PDF}")
    finally:
        conn.close()
        print("🏁 Extraction Phase Complete in Record Time!")

if __name__ == "__main__":
    extract_deterministically()