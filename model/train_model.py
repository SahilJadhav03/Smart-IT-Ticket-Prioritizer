"""
Training script for the IT ticket classifier.

This script loads the sample dataset, preprocesses the text, and trains
the ticket classifier model for priority prediction.
"""
import os
import pandas as pd
import sys
import logging

# Add parent directory to path to import from utils and model
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.text_preprocessing import preprocess_text, combine_title_description
from model.classifier import TicketClassifier

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def train_model():
    """
    Train the ticket classifier model using the sample dataset.
    """
    # Path to the dataset and model
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(script_dir, 'sample_tickets.csv')
    model_path = os.path.join(script_dir, 'ticket_classifier.pkl')
    
    logging.info(f"Loading dataset from {dataset_path}")
    
    # Load the dataset
    try:
        df = pd.read_csv(dataset_path)
        logging.info(f"Loaded {len(df)} tickets from dataset")
    except Exception as e:
        logging.error(f"Error loading dataset: {e}")
        return
    
    # Preprocess the text
    logging.info("Preprocessing ticket text...")
    processed_texts = []
    for _, row in df.iterrows():
        combined_text = combine_title_description(row['Title'], row['Description'])
        processed_texts.append(combined_text)
    
    # Create and train the classifier
    logging.info("Training the classifier...")
    classifier = TicketClassifier()
    classifier.train(processed_texts, df['Priority'].tolist())
    
    # Save the model
    logging.info(f"Saving model to {model_path}")
    classifier.save_model(model_path)
    logging.info("Model training complete")

if __name__ == "__main__":
    train_model()