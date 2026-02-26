# # # from flask import Flask, render_template, request, send_file, jsonify
# # # import os
# # # import subprocess

# # # app = Flask(__name__)

# # # # --- CONFIGURATION ---
# # # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# # # INPUT_ZONE = os.path.join(BASE_DIR, "../01_Input_Zone")
# # # OUTPUT_ZONE = os.path.join(BASE_DIR, "../07_Final_Output")
# # # FINAL_EXCEL = os.path.join(OUTPUT_ZONE, "Final_KTU_Results.xlsx")

# # # # --- ROUTES ---

# # # @app.route('/')
# # # def home():
# # #     """Renders the main page."""
# # #     return render_template('index.html')

# # # @app.route('/analyze', methods=['POST'])
# # # def analyze():
# # #     """Handles file upload and triggers the pipeline."""
# # #     if 'file' not in request.files:
# # #         return jsonify({"status": "error", "message": "No file uploaded"}), 400
    
# # #     file = request.files['file']
# # #     if file.filename == '':
# # #         return jsonify({"status": "error", "message": "No file selected"}), 400

# # #     # 1. Save the PDF
# # #     if not os.path.exists(INPUT_ZONE):
# # #         os.makedirs(INPUT_ZONE)
    
# # #     save_path = os.path.join(INPUT_ZONE, "sample_result.pdf")
# # #     file.save(save_path)
    
# # #     try:
# # #         # 2. Run the Pipeline (The same commands we used manually)
# # #         # Step A: Extractor
# # #         subprocess.run(["python", "extractor.py"], cwd="../02_Extraction_Engine", shell=True, check=True)
        
# # #         # Step B: Calculator
# # #         subprocess.run(["python", "calculator.py"], cwd="../04_Calculation_Core", shell=True, check=True)
        
# # #         # Step C: Exporter
# # #         subprocess.run(["python", "exporter.py"], cwd="../05_Excel_Generator", shell=True, check=True)
        
# # #         return jsonify({"status": "success", "message": "Analysis Complete!"})

# # #     except subprocess.CalledProcessError as e:
# # #         return jsonify({"status": "error", "message": f"Pipeline Failed: {str(e)}"}), 500
# # #     except Exception as e:
# # #         return jsonify({"status": "error", "message": f"Server Error: {str(e)}"}), 500

# # # @app.route('/download')
# # # def download_file():
# # #     """Sends the Excel file to the user."""
# # #     if os.path.exists(FINAL_EXCEL):
# # #         return send_file(FINAL_EXCEL, as_attachment=True)
# # #     else:
# # #         return "Error: File not generated yet.", 404

# # # if __name__ == '__main__':
# # #     app.run(debug=True, port=5000)


# # import os
# # import sys
# # import subprocess
# # from flask import Flask, request, jsonify, send_file, render_template

# # # Initialize Flask App
# # app = Flask(__name__, static_folder='static', template_folder='.')

# # # --- DYNAMIC PATHS ---
# # # This ensures the server always knows where the folders are, even on Render.com
# # BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# # INPUT_ZONE = os.path.join(BASE_DIR, '01_Input_Zone')
# # DB_PATH = os.path.join(BASE_DIR, '03_Database_Store', 'results.db')
# # OUTPUT_ZONE = os.path.join(BASE_DIR, '07_Final_Output')

# # @app.route('/')
# # def index():
# #     """Serves the main HTML interface."""
# #     return render_template('index.html')

# # # @app.route('/upload', methods=['POST'])
# # @app.route('/analyze', methods=['POST'])
# # def upload_file():
# #     """Handles the PDF upload and triggers the background Python engines."""
# #     if 'file' not in request.files:
# #         return jsonify({'error': 'No file uploaded'}), 400
    
# #     file = request.files['file']
# #     if file.filename == '':
# #         return jsonify({'error': 'No file selected'}), 400

# #     print("🌐 [SERVER] New PDF received! Starting pipeline...")

# #     # 1. Auto-Wipe: Clear the old database so we get fresh results for this specific PDF
# #     if os.path.exists(DB_PATH):
# #         os.remove(DB_PATH)
# #         print("🗑️ [SERVER] Cleared old database.")
        
# #     # 2. Save the uploaded PDF to the Input Zone
# #     pdf_path = os.path.join(INPUT_ZONE, 'sample_result.pdf')
# #     file.save(pdf_path)
# #     print(f"📥 [SERVER] Saved new PDF to {pdf_path}")

# #     try:
# #         # 3. Trigger the Extraction Engine
# #         # Change 'newextractor.py' to 'extractor.py' if you renamed the file back
# #         extractor_script = os.path.join(BASE_DIR, '02_Extraction_Engine', 'newextractor.py')
# #         print("⚙️ [SERVER] Triggering Extractor...")
# #         subprocess.run([sys.executable, extractor_script], check=True)

# #         # 4. Trigger the Excel Generator
# #         exporter_script = os.path.join(BASE_DIR, '05_Excel_Generator', 'exporter.py')
# #         print("📊 [SERVER] Triggering Exporter...")
# #         subprocess.run([sys.executable, exporter_script], check=True)

# #         return jsonify({'message': 'Processing complete!'}), 200

# #     except subprocess.CalledProcessError as e:
# #         print(f"❌ [SERVER] Pipeline crashed: {e}")
# #         return jsonify({'error': 'The processing engine failed.'}), 500

# # @app.route('/download/<filename>')
# # def download_file(filename):
# #     """Allows the user to download the final generated Excel sheets."""
# #     file_path = os.path.join(OUTPUT_ZONE, filename)
# #     if os.path.exists(file_path):
# #         return send_file(file_path, as_attachment=True)
# #     return jsonify({'error': 'File not found'}), 404

# # if __name__ == '__main__':
# #     # Runs the local development server
# #     app.run(debug=True, port=5000)


# import os
# import sys
# import subprocess
# from flask import Flask, request, jsonify, send_file, render_template

# app = Flask(__name__, static_folder='static', template_folder='.')

# # --- STRICT PATHING ---
# BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# INPUT_ZONE = os.path.join(BASE_DIR, '01_Input_Zone')
# DB_PATH = os.path.join(BASE_DIR, '03_Database_Store', 'results.db')
# OUTPUT_ZONE = os.path.join(BASE_DIR, '07_Final_Output')

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/analyze', methods=['POST'])
# def analyze():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file'}), 400
    
#     file = request.files['file']
    
#     # Auto-Wipe old data
#     if os.path.exists(DB_PATH):
#         os.remove(DB_PATH)
        
#     # Save PDF
#     if not os.path.exists(INPUT_ZONE): os.makedirs(INPUT_ZONE)
#     pdf_path = os.path.join(INPUT_ZONE, 'sample_result.pdf')
#     file.save(pdf_path)

#     try:
#         # Run Extraction
#         extractor_script = os.path.join(BASE_DIR, '02_Extraction_Engine', 'newextractor.py')
#         subprocess.run([sys.executable, extractor_script], check=True)

#         # Run Export
#         exporter_script = os.path.join(BASE_DIR, '05_Excel_Generator', 'exporter.py')
#         subprocess.run([sys.executable, exporter_script], check=True)

#         return jsonify({'status': 'success'}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/download/<filename>')
# def download_file(filename):
#     # This specifically looks into the 07_Final_Output folder
#     target_path = os.path.abspath(os.path.join(OUTPUT_ZONE, filename))
#     if os.path.exists(target_path):
#         return send_file(target_path, as_attachment=True)
#     return "File Not Found", 404

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)
import os
import sys
import subprocess
from flask import Flask, request, jsonify, send_file, render_template

app = Flask(__name__, static_folder='static', template_folder='.')

# --- ROBUST ABSOLUTE PATHS ---
FILE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(FILE_DIR, '..'))
INPUT_ZONE = os.path.join(BASE_DIR, '01_Input_Zone')
DB_PATH = os.path.join(BASE_DIR, '03_Database_Store', 'results.db')
OUTPUT_ZONE = os.path.join(BASE_DIR, '07_Final_Output')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    # 1. Ensure directories exist
    os.makedirs(INPUT_ZONE, exist_ok=True)
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    os.makedirs(OUTPUT_ZONE, exist_ok=True)

    # 2. Save PDF
    pdf_path = os.path.join(INPUT_ZONE, 'sample_result.pdf')
    file.save(pdf_path)

    try:
        # 3. Run Extractor
        ext_path = os.path.join(BASE_DIR, '02_Extraction_Engine', 'newextractor.py')
        subprocess.run([sys.executable, ext_path], check=True)

        # 4. Run Exporter
        exp_path = os.path.join(BASE_DIR, '05_Excel_Generator', 'exporter.py')
        subprocess.run([sys.executable, exp_path], check=True)

        return jsonify({'status': 'success'}), 200
    except Exception as e:
        print(f"Pipeline Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download(filename):
    file_path = os.path.abspath(os.path.join(OUTPUT_ZONE, filename))
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "File not found", 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)