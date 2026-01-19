from flask import Flask, render_template, request, send_file, jsonify
import os
import subprocess

app = Flask(__name__)

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_ZONE = os.path.join(BASE_DIR, "../01_Input_Zone")
OUTPUT_ZONE = os.path.join(BASE_DIR, "../07_Final_Output")
FINAL_EXCEL = os.path.join(OUTPUT_ZONE, "Final_KTU_Results.xlsx")

# --- ROUTES ---

@app.route('/')
def home():
    """Renders the main page."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Handles file upload and triggers the pipeline."""
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "error", "message": "No file selected"}), 400

    # 1. Save the PDF
    if not os.path.exists(INPUT_ZONE):
        os.makedirs(INPUT_ZONE)
    
    save_path = os.path.join(INPUT_ZONE, "sample_result.pdf")
    file.save(save_path)
    
    try:
        # 2. Run the Pipeline (The same commands we used manually)
        # Step A: Extractor
        subprocess.run(["python", "extractor.py"], cwd="../02_Extraction_Engine", shell=True, check=True)
        
        # Step B: Calculator
        subprocess.run(["python", "calculator.py"], cwd="../04_Calculation_Core", shell=True, check=True)
        
        # Step C: Exporter
        subprocess.run(["python", "exporter.py"], cwd="../05_Excel_Generator", shell=True, check=True)
        
        return jsonify({"status": "success", "message": "Analysis Complete!"})

    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "message": f"Pipeline Failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": f"Server Error: {str(e)}"}), 500

@app.route('/download')
def download_file():
    """Sends the Excel file to the user."""
    if os.path.exists(FINAL_EXCEL):
        return send_file(FINAL_EXCEL, as_attachment=True)
    else:
        return "Error: File not generated yet.", 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)