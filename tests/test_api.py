"""
API tests for the Flask application.
"""
import sys
import os
import unittest
import json
import tempfile

# Add the parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as flask_app
from model.train_model import train_model

class TestFlaskAPI(unittest.TestCase):
    """Test cases for the Flask API endpoints"""
    
    def setUp(self):
        """Set up the test environment"""
        # Configure the app for testing
        flask_app.app.config['TESTING'] = True
        flask_app.app.config['WTF_CSRF_ENABLED'] = False
        
        # Create a temporary database
        self.db_fd, flask_app.app.config['SQLALCHEMY_DATABASE_URI'] = tempfile.mkstemp()
        
        # Make sure we have a model for testing
        model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'model', 'ticket_classifier.pkl')
        if not os.path.exists(model_path):
            train_model()  # Train the model if it doesn't exist
        
        # Create a test client
        self.client = flask_app.app.test_client()
        
        # Initialize the database
        with flask_app.app.app_context():
            flask_app.db.create_all()
    
    def tearDown(self):
        """Clean up after testing"""
        os.close(self.db_fd)
        os.unlink(flask_app.app.config['SQLALCHEMY_DATABASE_URI'])
    
    def test_index_page(self):
        """Test the index page route"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Smart IT Ticket Prioritizer', response.data)
    
    def test_submit_page(self):
        """Test the submit page route"""
        response = self.client.get('/submit')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Submit a Support Ticket', response.data)
    
    def test_submit_ticket(self):
        """Test submitting a ticket"""
        response = self.client.post('/submit', data={
            'title': 'Test Ticket',
            'description': 'This is a test ticket description for testing the submission endpoint.'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        # Check that we were redirected to the index page
        self.assertIn(b'Recent Tickets', response.data)
        # Check that our ticket is now visible
        self.assertIn(b'Test Ticket', response.data)
    
    def test_missing_fields_submit(self):
        """Test submitting a ticket with missing fields"""
        response = self.client.post('/submit', data={
            'title': 'Test Ticket',
            # Missing description
        })
        
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Title and description are required', response.data)
    
    def test_api_classify(self):
        """Test the API classify endpoint"""
        test_data = {
            'title': 'Server Down',
            'description': 'Our main database server is not responding. Users cannot access any applications.'
        }
        
        response = self.client.post(
            '/api/classify',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Check that we got the expected fields in response
        self.assertIn('title', data)
        self.assertIn('priority', data)
        self.assertIn('team', data)
        
        # Check that the title is preserved
        self.assertEqual(data['title'], 'Server Down')
        
        # Check that priority is one of the valid options
        self.assertIn(data['priority'], ['Critical', 'High', 'Medium', 'Low'])
        
        # Check that team is one of the valid options
        self.assertIn(data['team'], ['network', 'hardware', 'software', 'security'])
    
    def test_api_missing_fields(self):
        """Test the API with missing fields"""
        # Missing description
        test_data = {
            'title': 'Server Down'
        }
        
        response = self.client.post(
            '/api/classify',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_view_tickets_page(self):
        """Test the view tickets page route"""
        # First add a ticket
        self.client.post('/submit', data={
            'title': 'Test Ticket for View',
            'description': 'This is a test ticket description for testing the view tickets page.'
        })
        
        # Then check the tickets page
        response = self.client.get('/tickets')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'All Support Tickets', response.data)
        self.assertIn(b'Test Ticket for View', response.data)


if __name__ == '__main__':
    unittest.main()