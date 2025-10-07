"""
Unit tests for the ticket classifier model.
"""
import sys
import os
import unittest
import tempfile

# Add the parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.classifier import TicketClassifier
from utils.text_preprocessing import preprocess_text

class TestTicketClassifier(unittest.TestCase):
    """Test cases for the ticket classifier"""
    
    def setUp(self):
        """Set up the test environment"""
        self.classifier = TicketClassifier()
        
        # Sample training data
        self.train_texts = [
            "server is down cannot access email critical issue",
            "website not loading for customers urgent problem",
            "need password reset for user account low priority",
            "printer not working in office",
            "internet connection slow for all employees",
            "virus detected on computer urgent security issue",
            "new software installation request for department",
            "keyboard broken need replacement",
            "email not sending messages medium priority"
        ]
        
        self.train_priorities = [
            "Critical",  # server down
            "Critical",  # website not loading
            "Low",       # password reset
            "Medium",    # printer not working
            "High",      # internet connection slow
            "High",      # virus detected
            "Low",       # software installation
            "Medium",    # keyboard broken
            "Medium"     # email not sending
        ]
        
        # Train the classifier
        self.classifier.train(self.train_texts, self.train_priorities)
    
    def test_priority_mapping(self):
        """Test the priority mapping functionality"""
        self.assertEqual(self.classifier.priority_mapping[0], 'Low')
        self.assertEqual(self.classifier.priority_mapping[1], 'Medium')
        self.assertEqual(self.classifier.priority_mapping[2], 'High')
        self.assertEqual(self.classifier.priority_mapping[3], 'Critical')
        
        self.assertEqual(self.classifier.reverse_priority_mapping['Low'], 0)
        self.assertEqual(self.classifier.reverse_priority_mapping['Medium'], 1)
        self.assertEqual(self.classifier.reverse_priority_mapping['High'], 2)
        self.assertEqual(self.classifier.reverse_priority_mapping['Critical'], 3)
    
    def test_predict_critical(self):
        """Test prediction of Critical priority"""
        test_texts = [
            "main database server crashed all systems down",
            "company website is not accessible to customers losing sales",
            "ransomware detected across network all files encrypted",
            "production system failure during business hours"
        ]
        
        for text in test_texts:
            with self.subTest(text=text):
                processed_text = preprocess_text(text)
                prediction = self.classifier.predict(processed_text)
                self.assertEqual(prediction, "Critical")
    
    def test_predict_high(self):
        """Test prediction of High priority"""
        test_texts = [
            "network connection very slow affecting multiple teams",
            "important application keeps crashing for sales team",
            "possible security breach detected in logs",
            "email server experiencing intermittent outages"
        ]
        
        for text in test_texts:
            with self.subTest(text=text):
                processed_text = preprocess_text(text)
                prediction = self.classifier.predict(processed_text)
                self.assertEqual(prediction, "High")
    
    def test_predict_medium(self):
        """Test prediction of Medium priority"""
        test_texts = [
            "printer not working in marketing department",
            "need software update for design team",
            "user cannot access shared drive",
            "monitor display showing strange colors"
        ]
        
        for text in test_texts:
            with self.subTest(text=text):
                processed_text = preprocess_text(text)
                prediction = self.classifier.predict(processed_text)
                self.assertEqual(prediction, "Medium")
    
    def test_predict_low(self):
        """Test prediction of Low priority"""
        test_texts = [
            "need help changing email signature",
            "requesting access to optional software",
            "question about using spreadsheet formulas",
            "need new mouse pad replacement"
        ]
        
        for text in test_texts:
            with self.subTest(text=text):
                processed_text = preprocess_text(text)
                prediction = self.classifier.predict(processed_text)
                self.assertEqual(prediction, "Low")
    
    def test_save_load_model(self):
        """Test saving and loading the model"""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            temp_path = temp.name
        
        try:
            # Save the model
            self.classifier.save_model(temp_path)
            
            # Create a new classifier and load the model
            new_classifier = TicketClassifier(temp_path)
            
            # Test that predictions are the same
            test_text = "server is down for maintenance"
            processed_text = preprocess_text(test_text)
            
            original_prediction = self.classifier.predict(processed_text)
            loaded_prediction = new_classifier.predict(processed_text)
            
            self.assertEqual(original_prediction, loaded_prediction)
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)


if __name__ == '__main__':
    unittest.main()