# 1. Start with a lightweight Linux Python environment
FROM python:3.10-slim

# 2. Install the heavy C++ OS libraries needed by Camelot and OpenCV
RUN apt-get update && apt-get install -y \
    ghostscript \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 3. Create a folder inside the virtual computer for our app
WORKDIR /app

# 4. Copy the requirements file first to install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your project files into the virtual computer
COPY . .

# 6. Open the port Render expects
EXPOSE 10000

# 7. Start the server using Gunicorn, pointing to your 06_Web_Interface folder
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "--timeout", "120", "06_Web_Interface.app:app"]