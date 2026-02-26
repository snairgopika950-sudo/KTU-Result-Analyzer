<<<<<<< Updated upstream
import sqlite3
=======
# # # import sqlite3
# # # import pandas as pd
# # # import os

# # # # --- CONFIGURATION ---
# # # DB_PATH = "../03_Database_Store/results.db"
# # # OUTPUT_FOLDER = "../07_Final_Output"
# # # OUTPUT_FILE = "Final_KTU_Results.xlsx"

# # # def generate_excel():
# # #     print(" Generating Excel Master Sheet...")
    
# # #     conn = sqlite3.connect(DB_PATH)
    
# # #     # 1. Load Data
# # #     query = "SELECT register_id, subject_code, grade, credits, points FROM results"
# # #     df = pd.read_sql(query, conn)
# # #     conn.close()

# # #     if df.empty:
# # #         print(" Error: Database is empty! Run extractor first.")
# # #         return

# # #     # --- AGGRESSIVE CLEANING (THE FIX) ---
# # #     # Strip invisible spaces from IDs and Subject Codes
# # #     df['register_id'] = df['register_id'].astype(str).str.strip()
# # #     df['subject_code'] = df['subject_code'].astype(str).str.strip()

# # #     # --- REMOVE DUPLICATES ---
# # #     # Keep the LAST entry found for every Student+Subject combo
# # #     initial_count = len(df)
# # #     df = df.drop_duplicates(subset=['register_id', 'subject_code'], keep='last')
# # #     final_count = len(df)
    
# # #     if initial_count > final_count:
# # #         print(f" Cleaned up {initial_count - final_count} duplicate records.")

# # #     # 2. Pivot the Data
# # #     # Row = Student, Cols = Subjects
# # #     try:
# # #         pivot_df = df.pivot(index='register_id', columns='subject_code', values='grade')
# # #     except ValueError as e:
# # #         print(f" Critical Error during Pivot: {e}")
# # #         print("Tip: You might need to delete 'results.db' and re-run extraction to clear bad data.")
# # #         return

# # #     # 3. Calculate SGPA
# # #     # Group by Register ID and sum credits/points
# # #     sums = df.groupby('register_id')[['credits', 'points']].sum()
    
# # #     # Calculate SGPA (Points / Credits)
# # #     sums['SGPA'] = sums.apply(lambda x: round(x['points'] / x['credits'], 2) if x['credits'] > 0 else 0, axis=1)

# # #     # 4. Find Failed Subjects
# # #     failures = df[df['grade'].isin(['F', 'Absent', 'FE'])]
# # #     failed_list = failures.groupby('register_id')['subject_code'].apply(lambda x: ', '.join(x))

# # #     # 5. Merge Everything
# # #     final_df = pivot_df.join(sums['SGPA'])  # Add SGPA column
# # #     final_df = final_df.join(failed_list.rename("FAILED_SUBJECTS")) # Add Failures column
    
# # #     # Fill NaN (Empty cells) with '-'
# # #     final_df = final_df.fillna('-')

# # #     # 6. Save to Excel with Formatting
# # #     if not os.path.exists(OUTPUT_FOLDER):
# # #         os.makedirs(OUTPUT_FOLDER)
        
# # #     save_path = os.path.join(OUTPUT_FOLDER, OUTPUT_FILE)
    
# # #     # We use ExcelWriter to apply styles
# # #     try:
# # #         with pd.ExcelWriter(save_path, engine='xlsxwriter') as writer:
# # #             final_df.to_excel(writer, sheet_name='Master_Sheet')
            
# # #             workbook = writer.book
# # #             worksheet = writer.sheets['Master_Sheet']
            
# # #             # Styles
# # #             header_fmt = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1})
# # #             fail_fmt = workbook.add_format({'font_color': 'red', 'bold': True})
            
# # #             # Apply header format
# # #             for col_num, value in enumerate(final_df.columns.values):
# # #                 worksheet.write(0, col_num + 1, value, header_fmt)

# # #             # Highlight FAILED_SUBJECTS column in Red
# # #             # Check if column exists first
# # #             if "FAILED_SUBJECTS" in final_df.columns:
# # #                 fail_col_idx = final_df.columns.get_loc("FAILED_SUBJECTS") + 1
# # #                 worksheet.set_column(fail_col_idx, fail_col_idx, 20, fail_fmt)

# # #         print(f" Success! Excel saved to: {os.path.abspath(save_path)}")
        
# # #     except Exception as e:
# # #         print(f" Error saving Excel: {e}")

# # # if __name__ == "__main__":
# # #     generate_excel()

# # import sqlite3
# # import pandas as pd
# # import os
# # import re

# # # --- CONFIGURATION ---
# # DB_PATH = "../03_Database_Store/results.db"
# # OUTPUT_FOLDER = "../07_Final_Output"
# # OUTPUT_FILE = "Final_KTU_Results.xlsx"

# # def get_batch_year(register_id):
# #     """
# #     Extracts the batch year from ID.
# #     Examples: 'CEK23CS061' -> 23, 'TVE20EC010' -> 20
# #     """
# #     # Regex looks for the first 2 digits after the first 3 letters
# #     match = re.search(r'[A-Z]{3}(\d{2})', str(register_id))
# #     if match:
# #         return int(match.group(1))
# #     return 0  # Default if pattern not found

# # def generate_excel():
# #     print(" Generating Excel Master Sheet with Batch Logic...")
    
# #     conn = sqlite3.connect(DB_PATH)
    
# #     # 1. Load Data
# #     query = "SELECT register_id, subject_code, grade, credits, points FROM results"
# #     df = pd.read_sql(query, conn)
# #     conn.close()

# #     if df.empty:
# #         print(" Error: Database is empty! Run extractor first.")
# #         return

# #     # --- CLEANING ---
# #     df['register_id'] = df['register_id'].astype(str).str.strip()
# #     df['subject_code'] = df['subject_code'].astype(str).str.strip()
    
# #     # Remove duplicates
# #     df = df.drop_duplicates(subset=['register_id', 'subject_code'], keep='last')

# #     # 2. Pivot Data (Rows to Columns)
# #     try:
# #         pivot_df = df.pivot(index='register_id', columns='subject_code', values='grade')
# #     except ValueError:
# #         print(" Error: Duplicate data found even after cleaning.")
# #         return

# #     # --- BATCH DETECTION LOGIC ---
# #     # A. Extract Year for every student
# #     # We create a temporary DataFrame for calculations
# #     calc_df = df.groupby('register_id')[['credits', 'points']].sum().reset_index()
# #     calc_df['Batch_Year'] = calc_df['register_id'].apply(get_batch_year)
    
# #     # B. Find the "Regular Class" (The Latest Year present in file)
# #     # If file has 20, 21, 22, 23 -> The Latest is 23.
# #     latest_batch = calc_df['Batch_Year'].max()
# #     print(f"🎓 Detected Regular Batch: 20{latest_batch}")

# #     # C. Calculate SGPA with Supply Filter
# #     def calculate_sgpa_safe(row):
# #         # RULE: Only calculate if Student belongs to Latest Batch
# #         if row['Batch_Year'] < latest_batch:
# #             return "Supply"  # It's a senior clearing backlogs
        
# #         # Normal Calculation
# #         if row['credits'] > 0:
# #             return round(row['points'] / row['credits'], 2)
# #         return 0

# #     calc_df['SGPA'] = calc_df.apply(calculate_sgpa_safe, axis=1)
    
# #     # Set Index for joining
# #     calc_df = calc_df.set_index('register_id')

# #     # 3. Find Failed Subjects
# #     failures = df[df['grade'].isin(['F', 'Absent', 'FE'])]
# #     failed_list = failures.groupby('register_id')['subject_code'].apply(lambda x: ', '.join(x))

# #     # 4. Merge Everything
# #     final_df = pivot_df.join(calc_df['SGPA'])  # Add SGPA
# #     final_df = final_df.join(failed_list.rename("FAILED_SUBJECTS")) # Add Failures
    
# #     # Fill NaN
# #     final_df = final_df.fillna('-')

# #     # 5. Save to Excel
# #     if not os.path.exists(OUTPUT_FOLDER):
# #         os.makedirs(OUTPUT_FOLDER)
        
# #     save_path = os.path.join(OUTPUT_FOLDER, OUTPUT_FILE)
    
# #     try:
# #         with pd.ExcelWriter(save_path, engine='xlsxwriter') as writer:
# #             final_df.to_excel(writer, sheet_name='Master_Sheet')
            
# #             workbook = writer.book
# #             worksheet = writer.sheets['Master_Sheet']
            
# #             # Styles
# #             header_fmt = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1})
# #             fail_fmt = workbook.add_format({'font_color': 'red', 'bold': True})
# #             supply_fmt = workbook.add_format({'font_color': '#808080', 'italic': True})
            
# #             # Headers
# #             for col_num, value in enumerate(final_df.columns.values):
# #                 worksheet.write(0, col_num + 1, value, header_fmt)

# #             # Highlight FAILED_SUBJECTS (Red)
# #             if "FAILED_SUBJECTS" in final_df.columns:
# #                 fail_col_idx = final_df.columns.get_loc("FAILED_SUBJECTS") + 1
# #                 worksheet.set_column(fail_col_idx, fail_col_idx, 20, fail_fmt)
            
# #             # Formatting "Supply" text in SGPA column
# #             # (Optional: Only if you want 'Supply' to look different)
# #             sgpa_col_idx = final_df.columns.get_loc("SGPA") + 1
# #             worksheet.set_column(sgpa_col_idx, sgpa_col_idx, 10)

# #         print(f"Success! Excel saved to: {os.path.abspath(save_path)}")
        
# #     except Exception as e:
# #         print(f" Error saving Excel: {e}")

# # if __name__ == "__main__":
# #     generate_excel()


# import sqlite3
# import pandas as pd
# import os
# import numpy as np

# # --- PATHS ---
# DB_PATH = os.path.join(os.path.dirname(__file__), '..', '03_Database_Store', 'results.db')
# OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', '07_Final_Output')

# # Create output directory if it doesn't exist
# os.makedirs(OUTPUT_DIR, exist_ok=True)

# # KTU 2019 Scheme Grade Points
# GRADE_POINTS = {
#     'S': 10, 'A+': 9, 'A': 8.5, 'B+': 8, 'B': 7.5, 
#     'C+': 7, 'C': 6.5, 'D': 6, 'P': 5.5, 'F': 0, 'FE': 0, 'Absent': 0
# }

# def get_credit_heuristic(subject_code):
#     """
#     Intelligently guesses credits if not in a syllabus file.
#     Labs (L), Seminars (Q), Projects (D) are usually 2 credits.
#     Standard Theory is usually 3 or 4 credits (we use 3 as a safe baseline).
#     """
#     code = subject_code.upper()
#     if 'L' in code or 'Q' in code or 'D' in code:
#         return 2
#     return 3 

# def generate_reports():
#     print("📊 Starting Calculation & Export Engine...")
    
#     # 1. Connect to Database and Load Data into Pandas
#     conn = sqlite3.connect(DB_PATH)
#     df = pd.read_sql_query("SELECT * FROM results", conn)
#     conn.close()

#     if df.empty:
#         print("❌ Error: Database is empty. Run extractor first.")
#         return

#     # 2. Apply Points and Credits mathematically
#     df['points'] = df['grade'].map(GRADE_POINTS).fillna(0)
#     df['credits'] = df['subject_code'].apply(get_credit_heuristic)
    
#     # Calculate Total Points earned for that specific subject
#     df['earned_points'] = df['points'] * df['credits']

#     # 3. Identify Regular vs Supply Batches
#     # The highest batch year (e.g., 23) is the current regular batch
#     current_batch_year = df['batch_year'].max()
#     print(f"🎯 Detected Current Regular Batch Year: 20{current_batch_year}")

#     regular_df = df[df['batch_year'] == current_batch_year]
#     supply_df = df[df['batch_year'] < current_batch_year]

#     # --- 4. PROCESS REGULAR STUDENTS (SGPA Calculation) ---
#     print(f"⚙️ Processing {regular_df['register_id'].nunique()} Regular Students...")
    
#     # Pivot the table so Subjects become Columns
#     reg_pivot = regular_df.pivot(index='register_id', columns='subject_code', values='grade').fillna('-')
    
#     # Group by student to calculate SGPA
#     # sgpa_calc = regular_df.groupby('register_id').apply(
#     #     lambda x: np.sum(x['earned_points']) / np.sum(x['credits']) if np.sum(x['credits']) > 0 else 0
#     # ).reset_index(name='SGPA')
#     sgpa_calc = regular_df.groupby('register_id').apply(
#         lambda x: np.sum(x['earned_points']) / np.sum(x['credits']) if np.sum(x['credits']) > 0 else 0,
#         include_groups=False
#     ).reset_index(name='SGPA')
#     # Round SGPA to 2 decimal places
#     sgpa_calc['SGPA'] = sgpa_calc['SGPA'].round(2)

#     # Merge SGPA back into the pivot table
#     final_regular_report = pd.merge(reg_pivot, sgpa_calc, on='register_id')

#     # Export Regular Batch
#     reg_path = os.path.join(OUTPUT_DIR, 'Regular_Batch_Results.xlsx')
#     final_regular_report.to_excel(reg_path, index=False)
#     print(f"✅ Generated: {reg_path}")

#     # --- 5. PROCESS SUPPLY STUDENTS (No SGPA) ---
#     if not supply_df.empty:
#         print(f"⚙️ Processing {supply_df['register_id'].nunique()} Supply Students...")
        
#         # For supply, we just show the subjects they attempted
#         sup_pivot = supply_df.pivot(index='register_id', columns='subject_code', values='grade').fillna('-')
        
#         sup_path = os.path.join(OUTPUT_DIR, 'Supply_Batch_Results.xlsx')
#         sup_pivot.to_excel(sup_path)
#         print(f"✅ Generated: {sup_path}")
#     else:
#         print("ℹ️ No supply students found in this dataset.")

# if __name__ == "__main__":
#     generate_reports()
>>>>>>> Stashed changes
import pandas as pd
import sqlite3
import os
<<<<<<< Updated upstream
=======
import numpy as np
import time
>>>>>>> Stashed changes

# --- UNIVERSAL ABSOLUTE PATHS ---
FILE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath(os.path.join(FILE_DIR, "../../03_Database_Store/results.db"))
OUTPUT_DIR = os.path.abspath(os.path.join(FILE_DIR, "../../07_Final_Output"))

<<<<<<< Updated upstream
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
        
=======
GRADE_POINTS = {
    'S': 10.0, 'A+': 9.0, 'A': 8.5, 'B+': 8.0, 
    'B': 7.0, 'C+': 6.0, 'C': 5.0, 'P': 4.0, 
    'F': 0.0, 'FE': 0.0, 'Absent': 0.0, 'I': 0.0
}

def get_ktu_credits(course_code):
    """Universal KTU 2019 Scheme Credit Logic"""
    code = str(course_code).upper().strip()
    if code.startswith('MAT'): return 4.0
    if code.startswith('MCN'): return 0.0
    # Labs, Seminars, Projects (Usually 2 credits)
    if len(code) >= 4:
        id_char = code[3] if not code[0].isdigit() else code[2]
        if id_char in ['L', 'Q', 'D']: return 2.0
    return 3.0

def calculate_ktu_sgpa(group):
    credit_courses = group[group['credits'] > 0].copy()
    if credit_courses.empty: return 0.0
    if any(g in ['F', 'FE', 'Absent', 'I'] for g in credit_courses['grade']):
        return 0.0
    total_w_points = np.sum(credit_courses['earned_points'])
    total_credits = np.sum(credit_courses['credits'])
    return round(total_w_points / total_credits, 2)

def run_export():
    # Wait up to 3 seconds for the extractor to finish writing the file
    for _ in range(3):
        if os.path.exists(DB_PATH): break
        time.sleep(1)

    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query("SELECT * FROM grades", conn)
>>>>>>> Stashed changes
    except Exception as e:
        print(f"⚠️ Table not ready yet: {e}")
        return
    finally:
        conn.close()

    if df.empty: return

    # Apply KTU Math
    df['credits'] = df['course_code'].apply(get_ktu_credits)
    df['grade_val'] = df['grade'].map(GRADE_POINTS).fillna(0.0)
    df['earned_points'] = df['grade_val'] * df['credits']

    # Batch Detection
    batch_series = df['register_id'].str.extract(r'(\d{2})')[0].dropna().astype(int)
    reg_year = batch_series.max() if not batch_series.empty else 0

    reg_df = df[df['register_id'].str.contains(f"\\D{reg_year}\\D", regex=True)]
    sup_df = df[~df['register_id'].str.contains(f"\\D{reg_year}\\D", regex=True)]

    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)

    for data, name in [(reg_df, "Regular"), (sup_df, "Supply")]:
        if not data.empty:
            pivot = data.pivot(index='register_id', columns='course_code', values='grade').fillna('-')
            sgpas = data.groupby('register_id').apply(calculate_ktu_sgpa, include_groups=False)
            pivot['SGPA'] = sgpas
            pivot.to_excel(os.path.join(OUTPUT_DIR, f"{name}_Batch_Results.xlsx"))
            print(f"✅ {name} Batch Exported Successfully.")

if __name__ == "__main__":
    run_export()