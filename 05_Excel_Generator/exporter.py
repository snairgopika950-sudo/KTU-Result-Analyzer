import sqlite3
import pandas as pd
import os

# --- CONFIGURATION ---
# DB_PATH = "../03_Database_Store/results.db"
# OUTPUT_FOLDER = "../07_Final_Output"
# OUTPUT_FILE = "Final_KTU_Results.xlsx"



# INPUT_FOLDER = "../01_Input_Zone"
# PDF_FILE = "sample_result.pdf"
# PDF_PATH = os.path.join(INPUT_FOLDER, PDF_FILE)
# OUTPUT_JSON = "raw_data.json"


import os

# --- ABSOLUTE PATH CALCULATION ---
# 1. Get the exact folder where exporter.py lives (.../05_Excel_Generator)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Go up one level to the main project root folder (.../KTU-Result-Analyzer)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

# 3. Define the unbreakable paths
DB_PATH = os.path.join(ROOT_DIR, "03_Database_Store", "results.db")
OUTPUT_FOLDER = os.path.join(ROOT_DIR, "07_Final_Output")
OUTPUT_FILE = "Final_KTU_Results.xlsx"

# Ensure the output folder actually exists before saving
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def generate_excel():
    print(" Generating Excel Master Sheet...")
    
    conn = sqlite3.connect(DB_PATH)
    
    # 1. Load Data
    query = "SELECT register_id, subject_code, grade, credits, points FROM results"
    df = pd.read_sql(query, conn)
    conn.close()

    if df.empty:
        print(" Error: Database is empty! Run extractor first.")
        return

    # --- AGGRESSIVE CLEANING (THE FIX) ---
    # Strip invisible spaces from IDs and Subject Codes
    df['register_id'] = df['register_id'].astype(str).str.strip()
    df['subject_code'] = df['subject_code'].astype(str).str.strip()

    # --- REMOVE DUPLICATES ---
    # Keep the LAST entry found for every Student+Subject combo
    initial_count = len(df)
    df = df.drop_duplicates(subset=['register_id', 'subject_code'], keep='last')
    final_count = len(df)
    
    if initial_count > final_count:
        print(f" Cleaned up {initial_count - final_count} duplicate records.")

    # 2. Pivot the Data
    # Row = Student, Cols = Subjects
    try:
        pivot_df = df.pivot(index='register_id', columns='subject_code', values='grade')
    except ValueError as e:
        print(f" Critical Error during Pivot: {e}")
        print("Tip: You might need to delete 'results.db' and re-run extraction to clear bad data.")
        return

    # 3. Calculate SGPA
    # Group by Register ID and sum credits/points
    sums = df.groupby('register_id')[['credits', 'points']].sum()
    
    # Calculate SGPA (Points / Credits)
    sums['SGPA'] = sums.apply(lambda x: round(x['points'] / x['credits'], 2) if x['credits'] > 0 else 0, axis=1)

    # 4. Find Failed Subjects
    failures = df[df['grade'].isin(['F', 'Absent', 'FE'])]
    failed_list = failures.groupby('register_id')['subject_code'].apply(lambda x: ', '.join(x))

    # 5. Merge Everything
    final_df = pivot_df.join(sums['SGPA'])  # Add SGPA column
    final_df = final_df.join(failed_list.rename("FAILED_SUBJECTS")) # Add Failures column
    
    # Fill NaN (Empty cells) with '-'
    final_df = final_df.fillna('-')

    # 6. Save to Excel with Formatting
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
        
    save_path = os.path.join(OUTPUT_FOLDER, OUTPUT_FILE)
    
    # We use ExcelWriter to apply styles
    try:
        with pd.ExcelWriter(save_path, engine='xlsxwriter') as writer:
            final_df.to_excel(writer, sheet_name='Master_Sheet')
            
            workbook = writer.book
            worksheet = writer.sheets['Master_Sheet']
            
            # Styles
            header_fmt = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1})
            fail_fmt = workbook.add_format({'font_color': 'red', 'bold': True})
            
            # Apply header format
            for col_num, value in enumerate(final_df.columns.values):
                worksheet.write(0, col_num + 1, value, header_fmt)

            # Highlight FAILED_SUBJECTS column in Red
            # Check if column exists first
            if "FAILED_SUBJECTS" in final_df.columns:
                fail_col_idx = final_df.columns.get_loc("FAILED_SUBJECTS") + 1
                worksheet.set_column(fail_col_idx, fail_col_idx, 20, fail_fmt)

        print(f" Success! Excel saved to: {os.path.abspath(save_path)}")
        
    except Exception as e:
        print(f" Error saving Excel: {e}")

if __name__ == "__main__":
    generate_excel()