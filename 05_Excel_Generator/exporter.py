# import sqlite3
# import pandas as pd
# import os

# # --- CONFIGURATION ---
# DB_PATH = "../03_Database_Store/results.db"
# OUTPUT_FOLDER = "../07_Final_Output"
# OUTPUT_FILE = "Final_KTU_Results.xlsx"

# def generate_excel():
#     print(" Generating Excel Master Sheet...")
    
#     conn = sqlite3.connect(DB_PATH)
    
#     # 1. Load Data
#     query = "SELECT register_id, subject_code, grade, credits, points FROM results"
#     df = pd.read_sql(query, conn)
#     conn.close()

#     if df.empty:
#         print(" Error: Database is empty! Run extractor first.")
#         return

#     # --- AGGRESSIVE CLEANING (THE FIX) ---
#     # Strip invisible spaces from IDs and Subject Codes
#     df['register_id'] = df['register_id'].astype(str).str.strip()
#     df['subject_code'] = df['subject_code'].astype(str).str.strip()

#     # --- REMOVE DUPLICATES ---
#     # Keep the LAST entry found for every Student+Subject combo
#     initial_count = len(df)
#     df = df.drop_duplicates(subset=['register_id', 'subject_code'], keep='last')
#     final_count = len(df)
    
#     if initial_count > final_count:
#         print(f" Cleaned up {initial_count - final_count} duplicate records.")

#     # 2. Pivot the Data
#     # Row = Student, Cols = Subjects
#     try:
#         pivot_df = df.pivot(index='register_id', columns='subject_code', values='grade')
#     except ValueError as e:
#         print(f" Critical Error during Pivot: {e}")
#         print("Tip: You might need to delete 'results.db' and re-run extraction to clear bad data.")
#         return

#     # 3. Calculate SGPA
#     # Group by Register ID and sum credits/points
#     sums = df.groupby('register_id')[['credits', 'points']].sum()
    
#     # Calculate SGPA (Points / Credits)
#     sums['SGPA'] = sums.apply(lambda x: round(x['points'] / x['credits'], 2) if x['credits'] > 0 else 0, axis=1)

#     # 4. Find Failed Subjects
#     failures = df[df['grade'].isin(['F', 'Absent', 'FE'])]
#     failed_list = failures.groupby('register_id')['subject_code'].apply(lambda x: ', '.join(x))

#     # 5. Merge Everything
#     final_df = pivot_df.join(sums['SGPA'])  # Add SGPA column
#     final_df = final_df.join(failed_list.rename("FAILED_SUBJECTS")) # Add Failures column
    
#     # Fill NaN (Empty cells) with '-'
#     final_df = final_df.fillna('-')

#     # 6. Save to Excel with Formatting
#     if not os.path.exists(OUTPUT_FOLDER):
#         os.makedirs(OUTPUT_FOLDER)
        
#     save_path = os.path.join(OUTPUT_FOLDER, OUTPUT_FILE)
    
#     # We use ExcelWriter to apply styles
#     try:
#         with pd.ExcelWriter(save_path, engine='xlsxwriter') as writer:
#             final_df.to_excel(writer, sheet_name='Master_Sheet')
            
#             workbook = writer.book
#             worksheet = writer.sheets['Master_Sheet']
            
#             # Styles
#             header_fmt = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1})
#             fail_fmt = workbook.add_format({'font_color': 'red', 'bold': True})
            
#             # Apply header format
#             for col_num, value in enumerate(final_df.columns.values):
#                 worksheet.write(0, col_num + 1, value, header_fmt)

#             # Highlight FAILED_SUBJECTS column in Red
#             # Check if column exists first
#             if "FAILED_SUBJECTS" in final_df.columns:
#                 fail_col_idx = final_df.columns.get_loc("FAILED_SUBJECTS") + 1
#                 worksheet.set_column(fail_col_idx, fail_col_idx, 20, fail_fmt)

#         print(f" Success! Excel saved to: {os.path.abspath(save_path)}")
        
#     except Exception as e:
#         print(f" Error saving Excel: {e}")

# if __name__ == "__main__":
#     generate_excel()

import sqlite3
import pandas as pd
import os
import re

# --- CONFIGURATION ---
DB_PATH = "../03_Database_Store/results.db"
OUTPUT_FOLDER = "../07_Final_Output"
OUTPUT_FILE = "Final_KTU_Results.xlsx"

def get_batch_year(register_id):
    """
    Extracts the batch year from ID.
    Examples: 'CEK23CS061' -> 23, 'TVE20EC010' -> 20
    """
    # Regex looks for the first 2 digits after the first 3 letters
    match = re.search(r'[A-Z]{3}(\d{2})', str(register_id))
    if match:
        return int(match.group(1))
    return 0  # Default if pattern not found

def generate_excel():
    print(" Generating Excel Master Sheet with Batch Logic...")
    
    conn = sqlite3.connect(DB_PATH)
    
    # 1. Load Data
    query = "SELECT register_id, subject_code, grade, credits, points FROM results"
    df = pd.read_sql(query, conn)
    conn.close()

    if df.empty:
        print(" Error: Database is empty! Run extractor first.")
        return

    # --- CLEANING ---
    df['register_id'] = df['register_id'].astype(str).str.strip()
    df['subject_code'] = df['subject_code'].astype(str).str.strip()
    
    # Remove duplicates
    df = df.drop_duplicates(subset=['register_id', 'subject_code'], keep='last')

    # 2. Pivot Data (Rows to Columns)
    try:
        pivot_df = df.pivot(index='register_id', columns='subject_code', values='grade')
    except ValueError:
        print(" Error: Duplicate data found even after cleaning.")
        return

    # --- BATCH DETECTION LOGIC ---
    # A. Extract Year for every student
    # We create a temporary DataFrame for calculations
    calc_df = df.groupby('register_id')[['credits', 'points']].sum().reset_index()
    calc_df['Batch_Year'] = calc_df['register_id'].apply(get_batch_year)
    
    # B. Find the "Regular Class" (The Latest Year present in file)
    # If file has 20, 21, 22, 23 -> The Latest is 23.
    latest_batch = calc_df['Batch_Year'].max()
    print(f"🎓 Detected Regular Batch: 20{latest_batch}")

    # C. Calculate SGPA with Supply Filter
    def calculate_sgpa_safe(row):
        # RULE: Only calculate if Student belongs to Latest Batch
        if row['Batch_Year'] < latest_batch:
            return "Supply"  # It's a senior clearing backlogs
        
        # Normal Calculation
        if row['credits'] > 0:
            return round(row['points'] / row['credits'], 2)
        return 0

    calc_df['SGPA'] = calc_df.apply(calculate_sgpa_safe, axis=1)
    
    # Set Index for joining
    calc_df = calc_df.set_index('register_id')

    # 3. Find Failed Subjects
    failures = df[df['grade'].isin(['F', 'Absent', 'FE'])]
    failed_list = failures.groupby('register_id')['subject_code'].apply(lambda x: ', '.join(x))

    # 4. Merge Everything
    final_df = pivot_df.join(calc_df['SGPA'])  # Add SGPA
    final_df = final_df.join(failed_list.rename("FAILED_SUBJECTS")) # Add Failures
    
    # Fill NaN
    final_df = final_df.fillna('-')

    # 5. Save to Excel
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
        
    save_path = os.path.join(OUTPUT_FOLDER, OUTPUT_FILE)
    
    try:
        with pd.ExcelWriter(save_path, engine='xlsxwriter') as writer:
            final_df.to_excel(writer, sheet_name='Master_Sheet')
            
            workbook = writer.book
            worksheet = writer.sheets['Master_Sheet']
            
            # Styles
            header_fmt = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1})
            fail_fmt = workbook.add_format({'font_color': 'red', 'bold': True})
            supply_fmt = workbook.add_format({'font_color': '#808080', 'italic': True})
            
            # Headers
            for col_num, value in enumerate(final_df.columns.values):
                worksheet.write(0, col_num + 1, value, header_fmt)

            # Highlight FAILED_SUBJECTS (Red)
            if "FAILED_SUBJECTS" in final_df.columns:
                fail_col_idx = final_df.columns.get_loc("FAILED_SUBJECTS") + 1
                worksheet.set_column(fail_col_idx, fail_col_idx, 20, fail_fmt)
            
            # Formatting "Supply" text in SGPA column
            # (Optional: Only if you want 'Supply' to look different)
            sgpa_col_idx = final_df.columns.get_loc("SGPA") + 1
            worksheet.set_column(sgpa_col_idx, sgpa_col_idx, 10)

        print(f"Success! Excel saved to: {os.path.abspath(save_path)}")
        
    except Exception as e:
        print(f" Error saving Excel: {e}")

if __name__ == "__main__":
    generate_excel()