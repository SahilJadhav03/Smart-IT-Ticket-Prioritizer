"""
Smart IT Ticket Prioritizer Flask Application

This is the main application file for the Smart IT Ticket Prioritizer.
It provides web routes and API endpoints for ticket submission and classification.
"""
import os
import sys
import logging
from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.exceptions import BadRequest
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add parent directory to path to import from other modules
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Import our modules
from utils.text_preprocessing import combine_title_description
from utils.team_assignment import get_team_assignment
from model.classifier import TicketClassifier
from database.models import init_db, db, Ticket

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Initialize Flask app
app = Flask(__name__)

# Configure app from environment variables
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-for-development')

# Initialize the database
init_db(app)

# Path to the trained model
MODEL_PATH = os.path.join(current_dir, 'model', 'ticket_classifier.pkl')

# Load the classifier model
classifier = TicketClassifier(MODEL_PATH)

@app.route('/')
def index():
    """
    Homepage route. Displays the ticket submission form and recent tickets.
    """
    # Fetch the most recent tickets from the database
    recent_tickets = Ticket.query.order_by(Ticket.created_at.desc()).limit(10).all()
    return render_template('index.html', tickets=recent_tickets)


@app.route('/submit', methods=['GET', 'POST'])
def submit_ticket():
    """
    Ticket submission route.
    GET: Show the submission form.
    POST: Process a new ticket submission.
    """
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title')
        description = request.form.get('description')
        
        if not title or not description:
            return render_template('submit.html', error='Title and description are required'), 400
        
        # Process the ticket
        priority, team, processed_text = process_ticket(title, description)
        
        # Save to database
        new_ticket = Ticket(
            title=title,
            description=description,
            priority=priority,
            team=team,
            processed_text=processed_text
        )
        
        db.session.add(new_ticket)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    # GET request - show the form
    return render_template('submit.html')


@app.route('/api/classify', methods=['POST'])
def classify_ticket_api():
    """
    API endpoint for ticket classification.
    Accepts JSON with title and description, returns priority and team.
    """
    try:
        # Get JSON data
        data = request.get_json()
        
        if not data:
            raise BadRequest("No JSON data received")
        
        title = data.get('title')
        description = data.get('description')
        
        if not title or not description:
            raise BadRequest("Title and description are required")
        
        # Process the ticket
        priority, team, processed_text = process_ticket(title, description)
        
        # Return the result
        return jsonify({
            'title': title,
            'priority': priority,
            'team': team
        })
        
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logging.error(f"Error processing API request: {e}")
        return jsonify({'error': 'An error occurred processing the ticket'}), 500


def process_ticket(title, description):
    """
    Process a ticket to determine priority and team assignment.
    
    Args:
        title (str): Ticket title
        description (str): Ticket description
        
    Returns:
        tuple: (priority, team, processed_text)
    """
    # Combine and preprocess text
    processed_text = combine_title_description(title, description)
    
    # Classify priority
    priority = classifier.predict(processed_text)
    
    # Assign team
    team = get_team_assignment(processed_text)
    
    return priority, team, processed_text


@app.route('/tickets')
def view_tickets():
    """
    View all tickets in the database.
    """
    tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
    return render_template('tickets.html', tickets=tickets)


@app.errorhandler(404)
def page_not_found(e):
    """
    Handle 404 errors.
    """
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    """
    Handle 500 errors.
    """
    logging.error(f"Server error: {e}")
    return render_template('500.html'), 500


if __name__ == '__main__':
    # Check if model exists
    if not os.path.exists(MODEL_PATH):
        logging.warning(f"Model not found at {MODEL_PATH}. Running training script...")
        from model.train_model import train_model
        train_model()
        logging.info("Model training completed.")
    
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app - debug mode only in development
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)