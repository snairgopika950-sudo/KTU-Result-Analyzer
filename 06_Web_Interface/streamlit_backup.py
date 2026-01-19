import streamlit as st
import os
import subprocess
import shutil

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_ZONE = os.path.join(BASE_DIR, "../01_Input_Zone")
OUTPUT_ZONE = os.path.join(BASE_DIR, "../07_Final_Output")
FINAL_EXCEL = os.path.join(OUTPUT_ZONE, "Final_KTU_Results.xlsx")

# Paths to your scripts (Remote Controls)
SCRIPT_EXTRACTOR = "../02_Extraction_Engine/extractor.py"
SCRIPT_LOADER = "../04_Calculation_Core/syllabus_loader.py"
SCRIPT_CALCULATOR = "../04_Calculation_Core/calculator.py"
SCRIPT_EXPORTER = "../05_Excel_Generator/exporter.py"

# --- PAGE SETUP ---
st.set_page_config(page_title="KTU Result Analyzer", page_icon="🎓", layout="centered")

st.title("🎓 KTU Result Analyzer")
st.markdown("### Transform PDF Results into Excel Analytics in Seconds")

# --- SIDEBAR: SYLLABUS SETTINGS ---
with st.sidebar:
    st.header(" Settings")
    st.info("Upload a Syllabus PDF here if you have new subjects (e.g., AI/ML courses).")
    syllabus_file = st.file_uploader("Upload Syllabus (Optional)", type="pdf")
    
    if syllabus_file:
        # Save syllabus to Input Zone
        save_path = os.path.join(INPUT_ZONE, "syllabus_upload.pdf")
        with open(save_path, "wb") as f:
            f.write(syllabus_file.getbuffer())
        st.success(" Syllabus Updated!")
        
        # Trigger Loader immediately
        with st.spinner("Learning new subjects..."):
            subprocess.run(["python", "syllabus_loader.py"], cwd="../04_Calculation_Core", shell=True)
        st.success("Credits Mapped!")

# --- MAIN AREA: RESULT PROCESSING ---
st.divider()
st.subheader("1️ Upload Result PDF")
uploaded_file = st.file_uploader("Drop your KTU Result PDF here", type="pdf")

if uploaded_file:
    # 1. Save the file to Input Zone
    if not os.path.exists(INPUT_ZONE):
        os.makedirs(INPUT_ZONE)
        
    target_path = os.path.join(INPUT_ZONE, "sample_result.pdf")
    with open(target_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f" File '{uploaded_file.name}' ready for processing.")

    # 2. The Magic Button
    if st.button(" Analyze Results", type="primary"):
        progress_bar = st.progress(0)
        status_text = st.empty()

        try:
            # STEP A: Extraction
            status_text.text(" Step 1/3: Extracting data from PDF...")
            subprocess.run(["python", "extractor.py"], cwd="../02_Extraction_Engine", shell=True, check=True)
            progress_bar.progress(33)

            # STEP B: Calculation
            status_text.text(" Step 2/3: Calculating SGPA & Credits...")
            subprocess.run(["python", "calculator.py"], cwd="../04_Calculation_Core", shell=True, check=True)
            progress_bar.progress(66)

            # STEP C: Excel Generation
            status_text.text(" Step 3/3: Generating Excel Report...")
            subprocess.run(["python", "exporter.py"], cwd="../05_Excel_Generator", shell=True, check=True)
            progress_bar.progress(100)
            
            status_text.text(" Processing Complete!")
            st.balloons()

            # 3. Download Button
            if os.path.exists(FINAL_EXCEL):
                with open(FINAL_EXCEL, "rb") as f:
                    st.download_button(
                        label="📥 Download Master Excel Sheet",
                        data=f,
                        file_name="KTU_Class_Results.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            else:
                st.error(" Error: Excel file was not generated.")

        except subprocess.CalledProcessError as e:
            st.error(f" An error occurred during processing. Check terminal for details.\nError: {e}")

st.divider()
st.caption("Built by Group 15 | KTU S5 Project")