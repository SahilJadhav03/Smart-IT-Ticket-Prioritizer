"""
Database configuration and setup for the Smart IT Ticket Prioritizer.

This module provides the SQLAlchemy database setup and connection.
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy
db = SQLAlchemy()

class Ticket(db.Model):
    """
    Ticket model for storing IT support tickets.
    """
    __tablename__ = 'tickets'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(50), nullable=False)  # Critical, High, Medium, Low
    team = db.Column(db.String(50), nullable=False)      # network, hardware, software, security
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_text = db.Column(db.Text)  # Preprocessed text for reference
    
    def __init__(self, title, description, priority, team, processed_text=None):
        """
        Initialize a new ticket.
        
        Args:
            title (str): Ticket title
            description (str): Ticket description
            priority (str): Ticket priority level
            team (str): Team assignment
            processed_text (str, optional): Preprocessed text used for classification
        """
        self.title = title
        self.description = description
        self.priority = priority
        self.team = team
        self.processed_text = processed_text
    
    def to_dict(self):
        """
        Convert the ticket to a dictionary.
        
        Returns:
            dict: Ticket data as dictionary
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'team': self.team,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


def init_db(app):
    """
    Initialize the database with the Flask app.
    
    Args:
        app: The Flask application
    """
    # Configure SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tickets.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize the app with the database
    db.init_app(app)
    
    # Create all tables
    with app.app_context():
        db.create_all()