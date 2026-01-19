# 🎓 KTU Result Analyzer & SGPA Calculator

> **Automated Result Parsing and Analytics System for APJ Abdul Kalam Technological University (KTU)**

![Project Status](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Framework](https://img.shields.io/badge/Framework-Flask-orange)

## 📖 Overview

The **KTU Result Analyzer** is a full-stack automated tool designed to eliminate the manual effort involved in calculating SGPA and analyzing class performance. 

Built for the **Computer Science (AI & ML)** branch, this system ingests raw Result PDFs published by the university, extracts student data using Regex pattern matching, maps credits dynamically using a learned Syllabus database, and generates a professional **Excel Master Sheet**.

It features a **"Safety Net" algorithm** that automatically detects Lab courses and specialized AI subjects, ensuring 100% calculation accuracy even for unknown subject codes.

---

## 🚀 Key Features

* **📄 PDF Data Extraction:** Uses `pdfplumber` and Regex to scrape Student IDs, Subject Codes, and Grades from unstructure university PDFs.
* **🧠 Intelligent Credit Mapping:**
    * Includes a master database of standard KTU subjects.
    * **Auto-Learning:** Can read a Syllabus PDF to "learn" new subject credits (e.g., specific AI/ML courses) on the fly.
    * **Heuristic Fallback:** Automatically identifies Lab courses (2 credits) vs. Theory courses (4 credits) if exact data is missing.
* **🗄️ Relational Data Storage:** Stores parsed data in a local **SQLite** database to handle duplicates and ensure data integrity.
* **📊 Automated Analytics:**
    * Calculates SGPA for every student.
    * Identifies failed subjects automatically.
* **📑 Excel Report Generation:** Exports a formatted Excel sheet with:
    * Pivoted data (Student vs. Subjects).
    * **Red Highlighting** for failed subjects.
    * SGPA columns.
* **💻 Modern Web Interface:** A custom HTML/CSS frontend powered by a Flask (Python) backend for a drag-and-drop experience.

---

## 🛠️ Technology Stack

| Component | Technology |
| :--- | :--- |
| **Backend Logic** | Python 3.x |
| **Web Framework** | Flask |
| **Database** | SQLite3 |
| **PDF Parsing** | pdfplumber, RegEx |
| **Data Analysis** | Pandas, NumPy |
| **Reporting** | XlsxWriter (Excel Automation) |
| **Frontend** | HTML5, CSS3, JavaScript |

---

## 📂 Project Structure

The project follows a modular "Pipeline" architecture:

```text
KTU_Result_Analyzer/
├── 01_Input_Zone/          # Raw PDF files (Results & Syllabus)
├── 02_Extraction_Engine/   # Script to parse PDF -> JSON
├── 03_Database_Store/      # SQLite Database Manager
├── 04_Calculation_Core/    # SGPA Logic & Credit Mapping
├── 05_Excel_Generator/     # Pandas Pivot & Excel Formatting
├── 06_Web_Interface/       # Flask App & HTML Templates
├── requirements.txt        # Dependencies
└── README.md               # Project Documentation
