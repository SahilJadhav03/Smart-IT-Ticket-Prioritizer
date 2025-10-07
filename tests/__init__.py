"""
Initialization file for the tests package.
Makes the package importable and allows running all tests.
"""
import unittest
import os
import sys

# Add the parent directory to the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_all_tests():
    """
    Run all tests in the tests package.
    """
    # Discover all test cases
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern="test_*.py")
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
    
if __name__ == '__main__':
    run_all_tests()