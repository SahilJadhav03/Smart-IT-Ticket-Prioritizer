"""
Definition of the model interface for ticket classification.

This module provides the TicketClassifier class that handles
loading, training, and predicting with the ticket classification model.
"""
import os
import pickle
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.linear_model import LogisticRegression

class TicketClassifier:
    """
    Class for ticket classification.
    
    Handles priority classification using a sklearn pipeline with TF-IDF
    vectorization and Logistic Regression classifier.
    """
    
    def __init__(self, model_path=None):
        """
        Initialize the TicketClassifier.
        
        Args:
            model_path (str, optional): Path to a saved model. If not provided, 
                                        a new model will be created.
        """
        self.priority_mapping = {
            0: 'Low',
            1: 'Medium',
            2: 'High',
            3: 'Critical'
        }
        
        self.reverse_priority_mapping = {v: k for k, v in self.priority_mapping.items()}
        
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
        else:
            # Create a new pipeline
            self.pipeline = Pipeline([
                ('vectorizer', TfidfVectorizer(max_features=5000)),
                ('classifier', MultiOutputClassifier(LogisticRegression(max_iter=1000)))
            ])
    
    def train(self, texts, priorities):
        """
        Train the classifier model.
        
        Args:
            texts (list): List of preprocessed ticket texts
            priorities (list): List of priority labels
            
        Returns:
            self: The trained classifier
        """
        # Convert priority strings to numeric values
        numeric_priorities = np.array([[self.reverse_priority_mapping[p]] for p in priorities])
        
        # Train the model
        self.pipeline.fit(texts, numeric_priorities)
        return self
    
    def predict(self, text):
        """
        Predict the priority of a ticket.
        
        Args:
            text (str): Preprocessed ticket text
            
        Returns:
            str: Predicted priority level
        """
        # Make prediction
        prediction = self.pipeline.predict([text])[0][0]
        
        # Convert numeric prediction to string label
        return self.priority_mapping[prediction]
    
    def save_model(self, model_path):
        """
        Save the model to disk.
        
        Args:
            model_path (str): Path where to save the model
        """
        with open(model_path, 'wb') as f:
            pickle.dump(self.pipeline, f)
    
    def load_model(self, model_path):
        """
        Load the model from disk.
        
        Args:
            model_path (str): Path to the saved model
        """
        with open(model_path, 'rb') as f:
            self.pipeline = pickle.load(f)