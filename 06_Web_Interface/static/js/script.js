const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const fileNameDisplay = document.getElementById('file-name');
const analyzeBtn = document.getElementById('analyze-btn');
const statusBox = document.getElementById('status-box');
const statusText = document.getElementById('status-text');
const downloadSection = document.getElementById('download-section');

let selectedFile = null;

// --- Drag & Drop Visuals ---
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('highlight');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('highlight');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('highlight');
    if (e.dataTransfer.files.length > 0) {
        handleFile(e.dataTransfer.files[0]);
    }
});

fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
        handleFile(fileInput.files[0]);
    }
});

function handleFile(file) {
    if (file.type !== 'application/pdf') {
        alert("Please upload a PDF file!");
        return;
    }
    selectedFile = file;
    fileNameDisplay.textContent = `📄 ${file.name}`;
    analyzeBtn.disabled = false;
}

// --- Button Click Logic ---
analyzeBtn.addEventListener('click', () => {
    if (!selectedFile) return;

    // UI Updates
    analyzeBtn.disabled = true;
    analyzeBtn.textContent = "Processing...";
    statusBox.style.display = "block";
    downloadSection.style.display = "none";
    statusText.textContent = "Uploading & Extracting Data...";

    const formData = new FormData();
    formData.append('file', selectedFile);

    // Send to Python Backend
    fetch('/analyze', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            statusText.textContent = "✅ Calculation Complete!";
            document.querySelector('.loader').style.display = 'none';
            downloadSection.style.display = 'block';
            analyzeBtn.textContent = "Analyze Another File";
            analyzeBtn.disabled = false;
        } else {
            statusText.textContent = "❌ Error: " + data.message;
            statusText.style.color = "red";
            analyzeBtn.disabled = false;
        }
    })
    .catch(error => {
        statusText.textContent = "❌ Server Connection Failed";
        console.error(error);
        analyzeBtn.disabled = false;
    });
});