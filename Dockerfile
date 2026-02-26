<<<<<<< HEAD
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
=======
# # 1. Start with a lightweight Linux Python environment
# FROM python:3.10-slim

# # 2. Install the heavy C++ OS libraries needed by Camelot and OpenCV
# RUN apt-get update && apt-get install -y \
#     ghostscript \
#     libgl1-mesa-glx \
#     libglib2.0-0 \
#     && rm -rf /var/lib/apt/lists/*

# # 3. Create a folder inside the virtual computer for our app
# WORKDIR /app

# # 4. Copy the requirements file first to install Python packages
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # 5. Copy the rest of your project files into the virtual computer
# COPY . .

# # 6. Open the port Render expects
# EXPOSE 10000

# # 7. Start the server using Gunicorn, pointing to your 06_Web_Interface folder
# CMD ["gunicorn", "--bind", "0.0.0.0:10000", "--timeout", "120", "06_Web_Interface.app:app"]
# 1. Use a specific, highly stable Debian release
FROM python:3.10-slim-bullseye

# 2. Use safety flags (--fix-missing) to bypass Linux network timeouts
RUN apt-get update -y --fix-missing && \
    apt-get install -y --no-install-recommends \
    ghostscript \
    libgl1 \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 3. Set the working directory
WORKDIR /app

# 4. Copy requirements and install Python libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy your project files
COPY . .

# 6. Start the server using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "--timeout", "120", "06_Web_Interface.app:app"]
>>>>>>> ca8a8c45c7e61ce4f97d05c5ce6be424975df447
