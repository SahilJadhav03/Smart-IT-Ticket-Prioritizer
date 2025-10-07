# Smart IT Ticket Prioritizer

A Flask-based web application that automatically classifies IT support tickets by priority level (Critical, High, Medium, Low) and assigns them to relevant teams using Natural Language Processing (NLP) and Machine Learning (ML) techniques.

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
   git clone https://github.com/yourusername/smart-ticket-prioritizer.git
   cd smart-ticket-prioritizer
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

## Usage

### Web Interface

1. **Submit a Ticket**:
   - Navigate to the "Submit Ticket" page
   - Fill in the ticket title and description
   - Submit the form to automatically classify and assign the ticket

2. **View Tickets**:
   - The homepage shows recent tickets
   - Use the "View All Tickets" page to see all tickets with filtering options

### API Usage

The application provides a REST API endpoint for programmatic ticket classification.

**Endpoint**: `/api/classify`

**Method**: POST

**Request Body**:
```json
{
  "title": "Cannot connect to WiFi",
  "description": "My laptop was working fine yesterday, but now I cannot connect to the company WiFi network."
}
```

**Response**:
```json
{
  "title": "Cannot connect to WiFi",
  "priority": "Medium",
  "team": "network"
}
```

Example using curl:
```
curl -X POST -H "Content-Type: application/json" -d '{"title": "Cannot connect to WiFi", "description": "My laptop was working fine yesterday, but now I cannot connect to the company WiFi network."}' http://127.0.0.1:5000/api/classify
```

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

## Model Training

The application includes a default trained model. If you want to retrain the model:

1. Modify the `model/sample_tickets.csv` file with your own training data
2. Run the training script:
   ```
   python -m model.train_model
   ```

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