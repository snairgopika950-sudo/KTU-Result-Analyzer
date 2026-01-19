import pdfplumber
import re
import os
import json  # <--- Added this

# --- CONFIGURATION ---
INPUT_FOLDER = "../01_Input_Zone"
PDF_FILE = "sample_result.pdf"
PDF_PATH = os.path.join(INPUT_FOLDER, PDF_FILE)
OUTPUT_JSON = "raw_data.json"  # <--- File to save data

# --- THE PATTERNS ---
STUDENT_ID_PATTERN = r"(CEK\w+)"
SUBJECT_GRADE_PATTERN = r"([A-Z]{3}\d{3})\(([^)]+)\)"

def extract_data():
    print(f" Opening PDF: {PDF_PATH}...")
    
    if not os.path.exists(PDF_PATH):
        print(" Error: File not found!")
        return

    extracted_data = []

    with pdfplumber.open(PDF_PATH) as pdf:
        total_pages = len(pdf.pages)
        print(f" Found {total_pages} pages. Scanning...")

        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue

            lines = text.split('\n')
            current_student = None
            
            for line in lines:
                student_match = re.search(STUDENT_ID_PATTERN, line)
                if student_match:
                    current_student = student_match.group(1)

                if current_student:
                    matches = re.findall(SUBJECT_GRADE_PATTERN, line)
                    for subject, grade in matches:
                        extracted_data.append({
                            "Register_ID": current_student,
                            "Subject_Code": subject,
                            "Grade": grade
                        })

    print(f"\n Extraction Complete! Found {len(extracted_data)} entries.")
    
    # --- SAVE TO JSON FILE ---
    with open(OUTPUT_JSON, "w") as f:
        json.dump(extracted_data, f, indent=4)
    print(f" Data saved to: {os.path.abspath(OUTPUT_JSON)}")

if __name__ == "__main__":
    extract_data()