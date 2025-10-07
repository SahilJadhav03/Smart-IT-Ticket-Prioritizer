# Smart IT Ticket Prioritizer

![Priority Levels](https://img.shields.io/badge/Priority%20Levels-4-blue)
![Teams](https://img.shields.io/badge/Teams-4-green)
![Python](https://img.shields.io/badge/Python-3.x-yellow)
![Flask](https://img.shields.io/badge/Flask-2.x-red)
![ML](https://img.shields.io/badge/ML-scikit--learn-orange)

A Flask-based web application that automatically classifies IT support tickets by priority level (Critical, High, Medium, Low) and assigns them to relevant teams using Natural Language Processing (NLP) and Machine Learning (ML) techniques. This tool helps IT departments efficiently manage and respond to support requests based on urgency and required expertise.

## Features

- **Smart Ticket Classification**: Automatically determines ticket priority based on content
- **Team Assignment**: Routes tickets to the appropriate team (Network, Hardware, Software, Security)
- **Web Interface**: Submit tickets through an easy-to-use web form
- **Dashboard View**: View and filter recent tickets by priority and team
- **REST API**: Classify tickets programmatically through a JSON API
- **SQLite Database**: Simple persistence for ticket storage

## Project Structure

```
Smart-Ticket-Prioritizer/
├── app.py                  # Flask application entry point
├── model/
│   ├── classifier.py       # ML classifier implementation
│   ├── sample_tickets.csv  # Training data
│   ├── ticket_classifier.pkl (generated)  # Trained model file
│   └── train_model.py      # Model training script
├── utils/
│   ├── text_preprocessing.py  # Text preprocessing utilities
│   └── team_assignment.py     # Team assignment logic
├── database/
│   └── models.py           # SQLAlchemy database models
├── templates/              # HTML templates
│   ├── index.html          # Homepage with recent tickets
│   ├── submit.html         # Ticket submission form
│   ├── tickets.html        # All tickets view
│   ├── 404.html            # Error page
│   └── 500.html            # Error page
├── static/
│   ├── css/
│   │   └── style.css       # CSS styles
│   └── js/
│       └── script.js       # JavaScript functionality
├── tests/                  # Unit tests
│   ├── test_text_preprocessing.py
│   ├── test_team_assignment.py
│   ├── test_classifier.py
│   └── test_api.py
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## Tech Stack

- **Python 3.x**: Core programming language
- **Flask**: Web framework for the application
- **scikit-learn**: Machine learning library for ticket classification
- **NLTK**: Natural Language Toolkit for text processing
- **SQLAlchemy**: ORM for database operations with SQLite
- **HTML/CSS/JavaScript**: Front-end interface

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/SahilJadhav03/Smart-ticket-it.git
   cd Smart-ticket-it
   ```

2. Create and activate a virtual environment:
   ```
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Train the model:
   ```
   python -m model.train_model
   ```

5. Run the application:
   ```
   python app.py
   ```

6. Access the application:
   Open your browser and navigate to `http://127.0.0.1:5000`

## How to Use the Tool

### Web Interface Walkthrough

1. **Submit a Ticket**:
   - Navigate to the "Submit Ticket" page by clicking the "Submit Ticket" link in the navigation bar
   - Fill in the ticket title with a concise description of the issue (e.g., "Cannot connect to WiFi")
   - Provide a detailed description in the description field (e.g., "My laptop was working fine yesterday, but now I cannot connect to the company WiFi network. I've tried restarting my computer but it didn't help.")
   - As you type, the system will show a real-time preview of the predicted priority and team assignment
   - Click the "Submit Ticket" button to create and classify your ticket
   - You'll be redirected to the homepage where you can see your newly created ticket

2. **View Tickets**:
   - The homepage shows the 10 most recent tickets with their priority levels and team assignments
   - Priority levels are color-coded: 
     - 🔴 Critical (Red): System-wide issues needing immediate attention
     - 🟠 High (Orange): Urgent issues affecting multiple users
     - 🟡 Medium (Yellow): Important issues affecting a few users
     - 🟢 Low (Green): Non-urgent requests or minor issues
   - Click on "View All Tickets" to see the complete ticket history
   - On the tickets page, you can:
     - Search for specific tickets using the search box
     - Filter tickets by priority (Critical, High, Medium, Low)
     - Filter tickets by team (Network, Hardware, Software, Security)
     - Click on ticket rows to see their full details

3. **Dashboard Features**:
   - Tickets are displayed with most recent first
   - Each ticket shows:
     - Title and a preview of the description
     - Priority level with color coding
     - Assigned team
     - Creation date and time
   - The tickets view provides a comprehensive overview of all IT support requests

### API Usage for Integration

The application provides a REST API endpoint for programmatic ticket classification, allowing you to integrate the classification system with other applications or services.

**Endpoint**: `/api/classify`

**Method**: POST

**Request Format**:
- Content-Type: application/json
- Required fields: `title` and `description`

**Request Body Example**:
```json
{
  "title": "Cannot connect to WiFi",
  "description": "My laptop was working fine yesterday, but now I cannot connect to the company WiFi network."
}
```

**Response Format**:
- Content-Type: application/json
- Returns: `title`, `priority`, and `team` fields

**Response Example**:
```json
{
  "title": "Cannot connect to WiFi",
  "priority": "Medium",
  "team": "network"
}
```

**Example API Call Using curl**:
```
curl -X POST -H "Content-Type: application/json" -d '{"title": "Cannot connect to WiFi", "description": "My laptop was working fine yesterday, but now I cannot connect to the company WiFi network."}' http://127.0.0.1:5000/api/classify
```

**Example API Call Using Python**:
```python
import requests
import json

url = "http://127.0.0.1:5000/api/classify"
data = {
    "title": "Cannot connect to WiFi",
    "description": "My laptop was working fine yesterday, but now I cannot connect to the company WiFi network."
}

response = requests.post(url, json=data)
result = response.json()
print(f"Priority: {result['priority']}, Team: {result['team']}")
```

**Error Handling**:
- If required fields are missing, the API returns a 400 Bad Request with an error message
- Server errors return a 500 status code with an error message

## Deployment

### Local Deployment with Environment Variables

For local development, create a `.env` file in the project root:

```
FLASK_ENV=development
DATABASE_URL=sqlite:///tickets.db
SECRET_KEY=your-secret-key-for-local-development
```

### Deploying to Render (Free)

1. Create a Render account at [render.com](https://render.com)

2. Connect your GitHub repository with Render

3. Create a new Web Service:
   - Select your GitHub repository
   - Use the following settings:
     - **Name**: Smart Ticket Prioritizer
     - **Environment**: Python
     - **Build Command**: `pip install -r requirements.txt && python -m nltk.downloader punkt stopwords wordnet && python -m model.train_model`
     - **Start Command**: `gunicorn app:app`

4. Add the following environment variables:
   - `FLASK_ENV`: production
   - `DATABASE_URL`: sqlite:///tickets.db
   - `SECRET_KEY`: (Generate a random string)

5. Deploy your application. Render will automatically build and deploy your app.

### Deploying to PythonAnywhere (Free)

1. Sign up for a free account at [PythonAnywhere](https://www.pythonanywhere.com/)

2. Clone your repository from GitHub:
   ```
   git clone https://github.com/yourusername/Smart-Ticket-Prioritizer.git
   ```

3. Create a virtual environment and install dependencies:
   ```
   mkvirtualenv --python=python3.9 ticketapp
   pip install -r requirements.txt
   python -m nltk.downloader punkt stopwords wordnet
   python -m model.train_model
   ```

4. Create a WSGI configuration file:
   - Go to the "Web" tab in PythonAnywhere
   - Click "Add a new web app"
   - Choose "Flask" and select your Python version
   - Set the path to your Flask app: `/home/yourusername/Smart-Ticket-Prioritizer/app.py`

5. Modify the WSGI file to include:
   ```python
   import sys
   import os
   
   path = '/home/yourusername/Smart-Ticket-Prioritizer'
   if path not in sys.path:
       sys.path.append(path)
   
   os.environ['SECRET_KEY'] = 'your-secret-key'
   os.environ['FLASK_ENV'] = 'production'
   os.environ['DATABASE_URL'] = 'sqlite:///tickets.db'
   
   from app import app as application
   ```

6. Reload your web app to apply changes.

### Deploying to Railway (Free)

1. Create an account at [Railway](https://railway.app/)

2. Install the Railway CLI:
   ```
   npm i -g @railway/cli
   ```

3. Login to Railway:
   ```
   railway login
   ```

4. Initialize your project:
   ```
   railway init
   ```

5. Deploy your application:
   ```
   railway up
   ```

6. Set the environment variables in the Railway dashboard:
   - `FLASK_ENV`: production
   - `DATABASE_URL`: sqlite:///tickets.db
   - `SECRET_KEY`: (Generate a random string)

## Running Tests

Execute the test suite to verify all components are working correctly:

```
python -m unittest discover tests
```

Or run individual test files:

```
python -m tests.test_api
python -m tests.test_classifier
python -m tests.test_text_preprocessing
python -m tests.test_team_assignment
```

## Example Ticket Classifications

See [EXAMPLES.md](EXAMPLES.md) for sample ticket classifications showing how the system categorizes different types of IT support requests by priority and team.

## Model Training and Customization

### Retraining the Model

The application includes a default trained model based on sample IT tickets. To retrain the model with your own data:

1. Modify the `model/sample_tickets.csv` file with your own training data
   - Keep the same format: ID, Title, Description, Priority, Team
   - Ensure priority levels are one of: Critical, High, Medium, Low
   - Ensure team assignments are one of: network, hardware, software, security

2. Run the training script:
   ```
   python -m model.train_model
   ```

3. The script will:
   - Load your custom ticket data
   - Preprocess the text using the NLP pipeline
   - Train a new classification model
   - Save the model to `model/ticket_classifier.pkl`
   - The new model will be used automatically the next time the application runs

### Customizing Priority Classification

The model uses a TF-IDF vectorizer with Logistic Regression to classify tickets. You can modify the classifier parameters in `model/classifier.py` to adjust:

- Feature extraction settings (max_features, ngram_range, etc.)
- Classification algorithm and parameters
- Priority thresholds and definitions

## Customization

### Priority Levels

Priority levels are defined in `model/classifier.py` and can be adjusted:

- Critical: Highest priority, system-wide issues
- High: Urgent issues affecting multiple users
- Medium: Important issues affecting a few users
- Low: Non-urgent requests or minor issues

### Team Assignment

Teams are defined in `utils/team_assignment.py` and can be customized by modifying the `TEAM_KEYWORDS` dictionary.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- NLTK for natural language processing tools
- scikit-learn for machine learning components
- Flask for the web framework