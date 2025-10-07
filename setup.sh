#!/bin/bash
# setup.sh - Setup script for Smart IT Ticket Prioritizer

# Check for Python
if command -v python3 &>/dev/null; then
    echo "Python 3 is installed"
else
    echo "Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
if [ -d "venv/bin" ]; then
    source venv/bin/activate
else
    source venv/Scripts/activate
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Train the model
echo "Training the classification model..."
python -m model.train_model

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    echo "FLASK_ENV=development" > .env
    echo "DATABASE_URL=sqlite:///tickets.db" >> .env
    echo "SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(16))')" >> .env
fi

echo "Setup complete! You can now run the application with: python app.py"