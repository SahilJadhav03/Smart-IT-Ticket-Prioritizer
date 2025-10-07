"""
Unit tests for text preprocessing utilities.
"""
import sys
import os
import unittest

# Add the parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.text_preprocessing import (
    clean_text,
    remove_stopwords,
    lemmatize_text,
    preprocess_text,
    combine_title_description
)

class TestTextPreprocessing(unittest.TestCase):
    """Test cases for text preprocessing functions"""
    
    def test_clean_text(self):
        """Test the clean_text function"""
        # Test basic cleaning
        text = "Hello, this is a TEST! 123 https://example.com"
        cleaned = clean_text(text)
        self.assertEqual(cleaned, "hello this is a test")
        
        # Test with None input
        cleaned = clean_text(None)
        self.assertEqual(cleaned, "")
        
        # Test with empty string
        cleaned = clean_text("")
        self.assertEqual(cleaned, "")
        
    def test_remove_stopwords(self):
        """Test the remove_stopwords function"""
        text = "this is a test for removing stopwords"
        result = remove_stopwords(text)
        # 'this', 'is', 'a', 'for' should be removed
        self.assertNotIn("this", result)
        self.assertNotIn("is", result)
        self.assertNotIn("a", result)
        self.assertNotIn("for", result)
        # 'test', 'removing', 'stopwords' should remain
        self.assertIn("test", result)
        self.assertIn("removing", result)
        self.assertIn("stopwords", result)
    
    def test_lemmatize_text(self):
        """Test the lemmatize_text function"""
        text = "running tests are showing results"
        result = lemmatize_text(text)
        # 'running' should be lemmatized to 'running' (as NLTK lemmatizes verbs by default)
        self.assertIn("running", result)
        # 'tests' should be lemmatized to 'test'
        self.assertIn("test", result)
        self.assertNotIn("tests", result)
        # 'showing' should remain as 'showing' (since NLTK lemmatizes nouns by default)
        self.assertIn("showing", result)
        # 'results' should be lemmatized to 'result'
        self.assertIn("result", result)
        self.assertNotIn("results", result)
    
    def test_preprocess_text(self):
        """Test the full preprocess_text pipeline"""
        text = "Running multiple Tests are showing Results! https://example.com"
        result = preprocess_text(text)
        # Check that text is lowercase
        self.assertNotIn("Running", result)
        self.assertNotIn("Tests", result)
        self.assertNotIn("Results", result)
        # Check that stopwords are removed
        self.assertNotIn("are", result)
        # Check that URL is removed
        self.assertNotIn("https", result)
        self.assertNotIn("example.com", result)
        # Check that text is lemmatized
        self.assertIn("test", result)
        self.assertNotIn("tests", result)
    
    def test_combine_title_description(self):
        """Test the combine_title_description function"""
        title = "Network Issue"
        description = "Cannot connect to the internet"
        result = combine_title_description(title, description)
        # Title should appear multiple times (weighted)
        self.assertGreater(result.count("network"), 1)
        # Description should be included
        self.assertIn("connect", result)
        self.assertIn("internet", result)


if __name__ == '__main__':
    unittest.main()