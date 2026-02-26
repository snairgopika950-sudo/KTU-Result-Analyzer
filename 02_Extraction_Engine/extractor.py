# # import pdfplumber
# # import re
# # import os
# # import json  # <--- Added this

# # # --- CONFIGURATION ---
# # INPUT_FOLDER = "../01_Input_Zone"
# # PDF_FILE = "sample_result.pdf"
# # PDF_PATH = os.path.join(INPUT_FOLDER, PDF_FILE)
# # OUTPUT_JSON = "raw_data.json"  # <--- File to save data

# # # --- THE PATTERNS ---
# # STUDENT_ID_PATTERN = r"(CEK\w+)"
# # SUBJECT_GRADE_PATTERN = r"([A-Z]{3}\d{3})\(([^)]+)\)"

# # def extract_data():
# #     print(f" Opening PDF: {PDF_PATH}...")
    
# #     if not os.path.exists(PDF_PATH):
# #         print(" Error: File not found!")
# #         return

# #     extracted_data = []

# #     with pdfplumber.open(PDF_PATH) as pdf:
# #         total_pages = len(pdf.pages)
# #         print(f" Found {total_pages} pages. Scanning...")

# #         for page in pdf.pages:
# #             text = page.extract_text()
# #             if not text:
# #                 continue

# #             lines = text.split('\n')
# #             current_student = None
            
# #             for line in lines:
# #                 student_match = re.search(STUDENT_ID_PATTERN, line)
# #                 if student_match:
# #                     current_student = student_match.group(1)

# #                 if current_student:
# #                     matches = re.findall(SUBJECT_GRADE_PATTERN, line)
# #                     for subject, grade in matches:
# #                         extracted_data.append({
# #                             "Register_ID": current_student,
# #                             "Subject_Code": subject,
# #                             "Grade": grade
# #                         })

# #     print(f"\n Extraction Complete! Found {len(extracted_data)} entries.")
    
# #     # --- SAVE TO JSON FILE ---
# #     with open(OUTPUT_JSON, "w") as f:
# #         json.dump(extracted_data, f, indent=4)
# #     print(f" Data saved to: {os.path.abspath(OUTPUT_JSON)}")

# # if __name__ == "__main__":
# #     extract_data()


# import pdfplumber
# import camelot
# import re
# import os
# import json
# import pandas as pd

# # --- CONFIGURATION (Kept exactly as requested) ---
# INPUT_FOLDER = "../01_Input_Zone"
# PDF_FILE = "sample_result.pdf"
# PDF_PATH = os.path.join(INPUT_FOLDER, PDF_FILE)
# OUTPUT_JSON = "raw_data.json"

# # --- THE PATTERNS (Refined for KTU format) ---
# STUDENT_ID_PATTERN = r"(CEK\w+)"
# # Pattern captures Subject(Grade) while handling potential whitespace
# SUBJECT_GRADE_PATTERN = r"([A-Z]{3}\d{3})\s*\(([^)]+)\)"

# def extract_data():
#     print(f"🚀 Starting Advanced Extraction on: {PDF_PATH}...")
    
#     if not os.path.exists(PDF_PATH):
#         print("❌ Error: File not found!")
#         return

#     extracted_data = []

#     # --- PHASE 1: PRECISION TABLE EXTRACTION (Camelot) ---
#     print("📋 Attempting Table-Aware Extraction (Camelot)...")
#     try:
#         # 'stream' flavor is best for KTU results which usually don't have visible grid lines
#         tables = camelot.read_pdf(PDF_PATH, pages='all', flavor='stream', edge_tol=50)
        
#         for i, table in enumerate(tables):
#             df = table.df
#             # Look at the accuracy report for this page
#             if table.parsing_report['accuracy'] > 90:
#                 for row in df.values:
#                     row_str = " ".join(map(str, row))
#                     # Find Student ID in the row
#                     student_match = re.search(STUDENT_ID_PATTERN, row_str)
#                     if student_match:
#                         student_id = student_match.group(1)
#                         # Find all Subject(Grade) pairs in that same row
#                         matches = re.findall(SUBJECT_GRADE_PATTERN, row_str)
#                         for subject, grade in matches:
#                             extracted_data.append({
#                                 "Register_ID": student_id.strip(),
#                                 "Subject_Code": subject.strip(),
#                                 "Grade": grade.strip()
#                             })
        
#         print(f"✅ Phase 1: Table extraction found {len(extracted_data)} entries.")

#     except Exception as e:
#         print(f"⚠️ Camelot failed or not configured: {e}. Falling back to text-based extraction.")

#     # --- PHASE 2: FALLBACK / REINFORCEMENT (pdfplumber) ---
#     # We run this only if camelot found nothing, or to double-check missing students
#     if len(extracted_data) == 0:
#         print("🔍 Running Fallback Regex Extraction (pdfplumber)...")
#         with pdfplumber.open(PDF_PATH) as pdf:
#             for page in pdf.pages:
#                 text = page.extract_text()
#                 if not text: continue

#                 lines = text.split('\n')
#                 current_student = None
                
#                 for line in lines:
#                     student_match = re.search(STUDENT_ID_PATTERN, line)
#                     if student_match:
#                         current_student = student_match.group(1)

#                     if current_student:
#                         matches = re.findall(SUBJECT_GRADE_PATTERN, line)
#                         for subject, grade in matches:
#                             entry = {
#                                 "Register_ID": current_student.strip(),
#                                 "Subject_Code": subject.strip(),
#                                 "Grade": grade.strip()
#                             }
#                             if entry not in extracted_data:
#                                 extracted_data.append(entry)

#     # --- PHASE 3: CLEANING & VALIDATION ---
#     # Filter out any malformed entries
#     valid_grades = ['S','A+','A','B+','B','C+','C','D','P','F','FE','I','Absent']
#     final_cleaned = [d for d in extracted_data if d['Grade'] in valid_grades]

#     print(f"\n✨ Extraction Complete! Found {len(final_cleaned)} verified entries.")
    
#     # --- SAVE TO JSON FILE ---
#     with open(OUTPUT_JSON, "w") as f:
#         json.dump(final_cleaned, f, indent=4)
#     print(f"📂 Data saved to: {os.path.abspath(OUTPUT_JSON)}")

# if __name__ == "__main__":
#     extract_data()

import pdfplumber
import camelot
import re
import os
import json
import pandas as pd

# --- CONFIGURATION (Kept exactly as requested) ---
# INPUT_FOLDER = "../01_Input_Zone"
# PDF_FILE = "sample_result.pdf"
# PDF_PATH = os.path.join(INPUT_FOLDER, PDF_FILE)
# OUTPUT_JSON = "raw_data.json"

# FILE_DIR = os.path.dirname(os.path.abspath(__file__))
# ROOT_DIR = os.path.abspath(os.path.join(FILE_DIR, ".."))

# OUTPUT_DIR = os.path.join(ROOT_DIR, "07_Final_Output")


import os

# --- ABSOLUTE PATH CALCULATION ---
# 1. Get the exact folder where this extractor.py script lives (.../02_Extraction_Engine)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Get the main project root folder (.../KTU-Result-Analyzer)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

# 3. Define the unbreakable path to the Input Zone
INPUT_FOLDER = os.path.join(ROOT_DIR, "01_Input_Zone")
PDF_FILE = "sample_result.pdf"
PDF_PATH = os.path.join(INPUT_FOLDER, PDF_FILE)

# 4. Save the JSON strictly inside the Extraction Engine folder
OUTPUT_JSON = os.path.join(CURRENT_DIR, "raw_data.json")


# --- THE PATTERNS (Refined for KTU format) ---
STUDENT_ID_PATTERN = r"(CEK\w+)"
# Pattern captures Subject(Grade) while handling potential whitespace
SUBJECT_GRADE_PATTERN = r"([A-Z]{3}\d{3})\s*\(([^)]+)\)"

def extract_data():
    print(f"🚀 Starting Advanced Extraction on: {PDF_PATH}...")
    
    if not os.path.exists(PDF_PATH):
        print("❌ Error: File not found!")
        return

    extracted_data = []

    # --- PHASE 1: PRECISION TABLE EXTRACTION (Camelot) ---
    print("📋 Attempting Table-Aware Extraction (Camelot)...")
    try:
        # 'stream' flavor is best for KTU results which usually don't have visible grid lines
        tables = camelot.read_pdf(PDF_PATH, pages='all', flavor='stream', edge_tol=50)
        
        for i, table in enumerate(tables):
            df = table.df
            # Look at the accuracy report for this page
            if table.parsing_report['accuracy'] > 90:
                for row in df.values:
                    row_str = " ".join(map(str, row))
                    # Find Student ID in the row
                    student_match = re.search(STUDENT_ID_PATTERN, row_str)
                    if student_match:
                        student_id = student_match.group(1)
                        # Find all Subject(Grade) pairs in that same row
                        matches = re.findall(SUBJECT_GRADE_PATTERN, row_str)
                        for subject, grade in matches:
                            extracted_data.append({
                                "Register_ID": student_id.strip(),
                                "Subject_Code": subject.strip(),
                                "Grade": grade.strip()
                            })
        
        print(f"✅ Phase 1: Table extraction found {len(extracted_data)} entries.")

    except Exception as e:
        print(f"⚠️ Camelot failed or not configured: {e}. Falling back to text-based extraction.")

    # --- PHASE 2: FALLBACK / REINFORCEMENT (pdfplumber) ---
    # We run this only if camelot found nothing, or to double-check missing students
    if len(extracted_data) == 0:
        print("🔍 Running Fallback Regex Extraction (pdfplumber)...")
        with pdfplumber.open(PDF_PATH) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if not text: continue

                lines = text.split('\n')
                current_student = None
                
                for line in lines:
                    student_match = re.search(STUDENT_ID_PATTERN, line)
                    if student_match:
                        current_student = student_match.group(1)

                    if current_student:
                        matches = re.findall(SUBJECT_GRADE_PATTERN, line)
                        for subject, grade in matches:
                            entry = {
                                "Register_ID": current_student.strip(),
                                "Subject_Code": subject.strip(),
                                "Grade": grade.strip()
                            }
                            if entry not in extracted_data:
                                extracted_data.append(entry)

    # --- PHASE 3: CLEANING & VALIDATION ---
    # Filter out any malformed entries
    valid_grades = ['S','A+','A','B+','B','C+','C','D','P','F','FE','I','Absent']
    final_cleaned = [d for d in extracted_data if d['Grade'] in valid_grades]

    print(f"\n✨ Extraction Complete! Found {len(final_cleaned)} verified entries.")
    
    # --- SAVE TO JSON FILE ---
    with open(OUTPUT_JSON, "w") as f:
        json.dump(final_cleaned, f, indent=4)
    print(f"📂 Data saved to: {os.path.abspath(OUTPUT_JSON)}")

if __name__ == "__main__":
    extract_data()