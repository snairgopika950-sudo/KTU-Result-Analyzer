# import os
# import sqlite3
# import pdfplumber
# import google.generativeai as genai
# import json
# import time
# from dotenv import load_dotenv

# # --- CONFIGURATION & SECURITY ---
# # Load the API key from the .env file in the main folder
# load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))
# API_KEY = os.environ.get("GEMINI_API_KEY")

# if not API_KEY:
#     raise ValueError("❌ CRITICAL: GEMINI_API_KEY not found in .env file.")

# genai.configure(api_key=API_KEY)

# # Use the 1.5-flash model. It is the fastest and most reliable for JSON extraction.
# model = genai.GenerativeModel(
#     "gemini-2.5-flash", generation_config={"response_mime_type": "application/json"}
# )

# # Paths
# INPUT_PDF = os.path.join(
#     os.path.dirname(__file__), "..", "01_Input_Zone", "sample_result.pdf"
# )
# DB_PATH = os.path.join(
#     os.path.dirname(__file__), "..", "03_Database_Store", "results.db"
# )

# # --- THE PROMPT ---
# SYSTEM_PROMPT = """
# You are a highly accurate academic data extraction system.
# Analyze the following raw text extracted from a university result PDF.
# Extract the student results and output ONLY a valid JSON array of objects.
# Do not hallucinate data. If a grade is missing, skip it.

# For each result, you must provide:
# - "register_id": The student's ID (e.g., "CEK23CS061")
# - "subject_code": The course code (e.g., "CST201")
# - "grade": The grade obtained (e.g., "B+", "F", "Absent")
# - "batch_year": Extract the two digits immediately following the first three letters of the register_id. (e.g., if ID is CEK23CS061, batch_year is 23. If ID is TVE22EC010, batch_year is 22).

# Output Format:
# [
#   {"register_id": "...", "subject_code": "...", "grade": "...", "batch_year": 23},
#   ...
# ]
# """


# def setup_database():
#     """Creates the SQLite table with the new batch_year column."""
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS results (
#             register_id TEXT,
#             subject_code TEXT,
#             grade TEXT,
#             batch_year INTEGER,
#             credits INTEGER DEFAULT 0,
#             points INTEGER DEFAULT 0,
#             PRIMARY KEY (register_id, subject_code)
#         )
#     """)
#     conn.commit()
#     return conn


# def extract_with_ai():
#     print("🤖 Starting AI Pre-Processing Pipeline...")
#     conn = setup_database()
#     cursor = conn.cursor()

#     try:
#         with pdfplumber.open(INPUT_PDF) as pdf:
#             total_pages = len(pdf.pages)
#             print(f"📄 Found PDF with {total_pages} pages.")

#             # Process in chunks of 3 pages to guarantee highest accuracy and avoid output truncation
#             chunk_size = 3
#             for i in range(0, total_pages, chunk_size):
#                 chunk_pages = pdf.pages[i : i + chunk_size]
#                 chunk_text = ""
#                 for page in chunk_pages:
#                     text = page.extract_text()
#                     if text:
#                         chunk_text += text + "\n"

#                 if not chunk_text.strip():
#                     continue

#                 print(
#                     f"⏳ Processing pages {i + 1} to {min(i + chunk_size, total_pages)} with Gemini AI..."
#                 )

#                 # Retry logic for Rate Limits (Error 429)
#                 max_retries = 3
#                 for attempt in range(max_retries):
#                     try:
#                         response = model.generate_content(
#                             SYSTEM_PROMPT + "\n\nRaw Text:\n" + chunk_text
#                         )

#                         # Parse the strict JSON response
#                         extracted_data = json.loads(response.text)

#                         # Insert into database, ignoring duplicates
#                         inserted_count = 0
#                         for row in extracted_data:
#                             try:
#                                 cursor.execute(
#                                     """
#                                     INSERT OR IGNORE INTO results
#                                     (register_id, subject_code, grade, batch_year)
#                                     VALUES (?, ?, ?, ?)
#                                 """,
#                                     (
#                                         row["register_id"],
#                                         row["subject_code"],
#                                         row["grade"],
#                                         row["batch_year"],
#                                     ),
#                                 )
#                                 if cursor.rowcount > 0:
#                                     inserted_count += 1
#                             except Exception as e:
#                                 print(f"⚠️ Skipping row due to DB error: {e}")

#                         conn.commit()
#                         print(
#                             f"✅ Successfully saved {inserted_count} new records to database."
#                         )
#                         break  # Break out of the retry loop if successful

#                     except Exception as ai_error:
#                         if "429" in str(ai_error) or "quota" in str(ai_error).lower():
#                             wait_time = 5 * (attempt + 1)
#                             print(
#                                 f"⚠️ Rate limit hit. Waiting {wait_time} seconds before retrying..."
#                             )
#                             time.sleep(wait_time)
#                         else:
#                             print(f"❌ AI Error on these pages: {ai_error}")
#                             break  # Break out of retry if it's a non-rate-limit error

#                 # Small sleep between chunks to respect free-tier limits
#                 time.sleep(2)

#     except FileNotFoundError:
#         print(f"❌ Error: Could not find PDF file at {INPUT_PDF}")
#     finally:
#         conn.close()
#         print("🏁 AI Extraction Phase Complete!")


# if __name__ == "__main__":
#     extract_with_ai()


# import os
# import sqlite3
# import pdfplumber
# from google import genai
# from google.genai import types
# import json
# import time
# from dotenv import load_dotenv

# # --- CONFIGURATION & SECURITY ---
# load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
# API_KEY = os.environ.get("GEMINI_API_KEY")

# if not API_KEY:
#     raise ValueError("❌ CRITICAL: GEMINI_API_KEY not found in .env file.")

# # Initialize the NEW Google GenAI client
# client = genai.Client(api_key=API_KEY)

# # Paths
# INPUT_PDF = os.path.join(os.path.dirname(__file__), '..', '01_Input_Zone', 'sample_result.pdf')
# DB_PATH = os.path.join(os.path.dirname(__file__), '..', '03_Database_Store', 'results.db')

# # --- THE PROMPT ---
# SYSTEM_PROMPT = """
# You are a highly accurate academic data extraction system.
# Analyze the following raw text extracted from a university result PDF.
# Extract the student results and output ONLY a valid JSON array of objects.
# Do not hallucinate data. If a grade is missing, skip it.

# For each result, you must provide:
# - "register_id": The student's ID (e.g., "CEK23CS061")
# - "subject_code": The course code (e.g., "CST201")
# - "grade": The grade obtained (e.g., "B+", "F", "Absent")
# - "batch_year": Extract the two digits immediately following the first three letters of the register_id. (e.g., if ID is CEK23CS061, batch_year is 23).

# Output Format:
# [
#   {"register_id": "...", "subject_code": "...", "grade": "...", "batch_year": 23}
# ]
# """

# def setup_database():
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS results (
#             register_id TEXT,
#             subject_code TEXT,
#             grade TEXT,
#             batch_year INTEGER,
#             credits INTEGER DEFAULT 0,
#             points INTEGER DEFAULT 0,
#             PRIMARY KEY (register_id, subject_code)
#         )
#     ''')
#     conn.commit()
#     return conn

# def extract_with_ai():
#     print("🤖 Starting AI Pre-Processing Pipeline...")
#     conn = setup_database()
#     cursor = conn.cursor()

#     try:
#         with pdfplumber.open(INPUT_PDF) as pdf:
#             total_pages = len(pdf.pages)
#             print(f"📄 Found PDF with {total_pages} pages.")

#             # Send 5 pages at a time. Gemini has a massive context window,
#             # so larger chunks = fewer API calls = no rate limit crashes.
#             chunk_size = 5
#             for i in range(0, total_pages, chunk_size):
#                 chunk_pages = pdf.pages[i:i + chunk_size]
#                 chunk_text = ""
#                 for page in chunk_pages:
#                     text = page.extract_text()
#                     if text:
#                         chunk_text += text + "\n"

#                 if not chunk_text.strip():
#                     continue

#                 print(f"⏳ Processing pages {i+1} to {min(i+chunk_size, total_pages)} with Gemini AI...")

#                 max_retries = 3
#                 for attempt in range(max_retries):
#                     try:
#                         # NEW SDK syntax for generating structured JSON content
#                         response = client.models.generate_content(
#                             model='gemini-2.5-flash',
#                             contents=SYSTEM_PROMPT + "\n\nRaw Text:\n" + chunk_text,
#                             config=types.GenerateContentConfig(
#                                 response_mime_type="application/json",
#                             )
#                         )

#                         extracted_data = json.loads(response.text)

#                         inserted_count = 0
#                         for row in extracted_data:
#                             try:
#                                 # Using .get() prevents crashes if the AI slightly changes a key name
#                                 cursor.execute('''
#                                     INSERT OR IGNORE INTO results
#                                     (register_id, subject_code, grade, batch_year)
#                                     VALUES (?, ?, ?, ?)
#                                 ''', (row.get('register_id'), row.get('subject_code'), row.get('grade'), row.get('batch_year')))
#                                 if cursor.rowcount > 0:
#                                     inserted_count += 1
#                             except Exception as e:
#                                 print(f"⚠️ DB Error: {e}")

#                         conn.commit()
#                         print(f"✅ Successfully saved {inserted_count} new records to database.")
#                         break

#                     except Exception as ai_error:
#                         if '429' in str(ai_error) or 'quota' in str(ai_error).lower() or 'exhausted' in str(ai_error).lower():
#                             # Exponential backoff for rate limits
#                             wait_time = 15 * (attempt + 1)
#                             print(f"⚠️ Rate limit hit. Waiting {wait_time} seconds before retrying...")
#                             time.sleep(wait_time)
#                         else:
#                             print(f"❌ AI Error: {ai_error}")
#                             break

#                 # Crucial 10-second sleep between successful chunks to protect the 15 RPM limit
#                 time.sleep(10)

#     except FileNotFoundError:
#         print(f"❌ Error: Could not find PDF file at {INPUT_PDF}")
#     finally:
#         conn.close()
#         print("🏁 AI Extraction Phase Complete!")

# if __name__ == "__main__":
#     extract_with_ai()


import os
import sqlite3
import pdfplumber
from google import genai
from google.genai import types
import json
import time
from dotenv import load_dotenv

# --- CONFIGURATION & SECURITY ---
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("❌ CRITICAL: GEMINI_API_KEY not found in .env file.")

client = genai.Client(api_key=API_KEY)

INPUT_PDF = os.path.join(
    os.path.dirname(__file__), "..", "01_Input_Zone", "sample_result.pdf"
)
DB_PATH = os.path.join(
    os.path.dirname(__file__), "..", "03_Database_Store", "results.db"
)

# --- THE PROMPT ---
SYSTEM_PROMPT = """
You are a highly accurate academic data extraction system.
Analyze the following raw text extracted from a university result PDF.
Extract the student results and output ONLY a valid JSON array of objects.
Do not hallucinate data. If a grade is missing, skip it.

For each result, you must provide:
- "register_id": The student's ID (e.g., "CEK23CS061")
- "subject_code": The course code (e.g., "CST201")
- "grade": The grade obtained (e.g., "B+", "F", "Absent")
- "batch_year": Extract the two digits immediately following the first three letters of the register_id. (e.g., if ID is CEK23CS061, batch_year is 23).

Output Format:
[
  {"register_id": "...", "subject_code": "...", "grade": "...", "batch_year": 23}
]
"""


def setup_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            register_id TEXT,
            subject_code TEXT,
            grade TEXT,
            batch_year INTEGER,
            credits INTEGER DEFAULT 0,
            points INTEGER DEFAULT 0,
            PRIMARY KEY (register_id, subject_code)
        )
    """)
    conn.commit()
    return conn


def extract_with_ai():
    print("🤖 Starting AI Pre-Processing Pipeline (Micro-Chunking Mode)...")
    conn = setup_database()
    cursor = conn.cursor()

    try:
        with pdfplumber.open(INPUT_PDF) as pdf:
            total_pages = len(pdf.pages)
            print(f"📄 Found PDF with {total_pages} pages.")

            # CHANGED: Process exactly ONE page at a time to prevent Token Payload Overload
            chunk_size = 1
            for i in range(0, total_pages, chunk_size):
                page = pdf.pages[i]
                chunk_text = page.extract_text()

                if not chunk_text or not chunk_text.strip():
                    print(f"⏭️ Skipping page {i + 1} (Empty or unreadable text).")
                    continue

                print(f"⏳ Processing Page {i + 1} of {total_pages} with Gemini AI...")

                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        # # CHANGED: Using the highly stable 1.5-flash-8b model for free tiers
                        # response = client.models.generate_content(
                        #     model="gemini-1.5-flash-8b",
                        #     contents=SYSTEM_PROMPT + "\n\nRaw Text:\n" + chunk_text,
                        #     config=types.GenerateContentConfig(
                        #         response_mime_type="application/json",
                        #     ),
                        # )
                        
                        # CHANGED: Using the currently active 2.0 free-tier model
                        response = client.models.generate_content(
                            model='gemini-2.0-flash', 
                            contents=SYSTEM_PROMPT + "\n\nRaw Text:\n" + chunk_text,
                            config=types.GenerateContentConfig(
                                response_mime_type="application/json",
                            )
                        )

                        extracted_data = json.loads(response.text)

                        inserted_count = 0
                        for row in extracted_data:
                            try:
                                cursor.execute(
                                    """
                                    INSERT OR IGNORE INTO results 
                                    (register_id, subject_code, grade, batch_year)
                                    VALUES (?, ?, ?, ?)
                                """,
                                    (
                                        row.get("register_id"),
                                        row.get("subject_code"),
                                        row.get("grade"),
                                        row.get("batch_year"),
                                    ),
                                )
                                if cursor.rowcount > 0:
                                    inserted_count += 1
                            except Exception as e:
                                pass  # Ignore duplicate DB errors silently

                        conn.commit()
                        print(
                            f"✅ Page {i + 1} Success: Saved {inserted_count} records."
                        )
                        break  # Break retry loop on success

                    except Exception as ai_error:
                        if (
                            "429" in str(ai_error)
                            or "quota" in str(ai_error).lower()
                            or "exhausted" in str(ai_error).lower()
                        ):
                            wait_time = 15 * (attempt + 1)
                            # CHANGED: Now printing the exact Google error reason
                            print(f"⚠️ Rate limit hit. Google says: {ai_error}")
                            print(
                                f"⏳ Pausing for {wait_time} seconds before retrying..."
                            )
                            time.sleep(wait_time)
                        else:
                            print(f"❌ AI Parsing Error on Page {i + 1}: {ai_error}")
                            break

                # CHANGED: A forced 5-second cooldown between every page to reset Google's spam filters
                time.sleep(5)

    except FileNotFoundError:
        print(f"❌ Error: Could not find PDF file at {INPUT_PDF}")
    finally:
        conn.close()
        print("🏁 AI Extraction Phase Complete!")


if __name__ == "__main__":
    extract_with_ai()
