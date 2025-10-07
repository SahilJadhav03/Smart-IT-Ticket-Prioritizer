# setup.ps1 - Setup script for Smart IT Ticket Prioritizer

# Check for Python
try {
    $pythonVersion = python --version
    Write-Host "Python is installed: $pythonVersion"
}
catch {
    Write-Host "Python is not installed. Please install Python 3 first."
    exit 1
}

# Create virtual environment
Write-Host "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
Write-Host "Activating virtual environment..."
.\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing dependencies..."
pip install -r requirements.txt

# Train the model
Write-Host "Training the classification model..."
python -m model.train_model

# Create .env file if it doesn't exist
if (-not (Test-Path .env)) {
    Write-Host "Creating .env file..."
    $secretKey = -join ((48..57) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
    Set-Content -Path .env -Value "FLASK_ENV=development`nDATABASE_URL=sqlite:///tickets.db`nSECRET_KEY=$secretKey"
}

Write-Host "Setup complete! You can now run the application with: python app.py"