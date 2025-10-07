"""
Text preprocessing utilities for the Smart IT Ticket Prioritizer.

This module provides functions for cleaning and preprocessing text data
before feeding it to machine learning models.
"""
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download required NLTK resources
def download_nltk_resources():
    """
    Download required NLTK resources if they aren't already available.
    """
    resources = ['punkt', 'stopwords', 'wordnet']
    for resource in resources:
        try:
            nltk.data.find(f'tokenizers/{resource}')
        except LookupError:
            nltk.download(resource, quiet=True)

# Make sure we have the required NLTK data
download_nltk_resources()

def clean_text(text):
    """
    Clean the text by removing special characters and converting to lowercase.
    
    Args:
        text (str): The text to clean
        
    Returns:
        str: Cleaned text
    """
    if not isinstance(text, str):
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove special characters and punctuation
    text = re.sub(r'[^\w\s]', '', text)
    
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def remove_stopwords(text):
    """
    Remove stopwords from the text.
    
    Args:
        text (str): The text to process
        
    Returns:
        str: Text without stopwords
    """
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    filtered_text = [word for word in word_tokens if word not in stop_words]
    return ' '.join(filtered_text)

def lemmatize_text(text):
    """
    Lemmatize the text to reduce words to their base form.
    
    Args:
        text (str): The text to lemmatize
        
    Returns:
        str: Lemmatized text
    """
    lemmatizer = WordNetLemmatizer()
    word_tokens = word_tokenize(text)
    lemmatized_text = [lemmatizer.lemmatize(word) for word in word_tokens]
    return ' '.join(lemmatized_text)

def preprocess_text(text):
    """
    Apply full preprocessing pipeline to the text.
    
    Args:
        text (str): The text to preprocess
        
    Returns:
        str: Fully preprocessed text
    """
    text = clean_text(text)
    text = remove_stopwords(text)
    text = lemmatize_text(text)
    return text

def combine_title_description(title, description):
    """
    Combine ticket title and description with appropriate weighting.
    Title is repeated to give it more weight in the classification.
    
    Args:
        title (str): The ticket title
        description (str): The ticket description
        
    Returns:
        str: Combined and preprocessed text
    """
    # Repeat title to increase its weight in the classification
    combined_text = title + " " + title + " " + description
    return preprocess_text(combined_text)