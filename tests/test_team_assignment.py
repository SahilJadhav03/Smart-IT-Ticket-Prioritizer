"""
Unit tests for the team assignment functionality.
"""
import sys
import os
import unittest

# Add the parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.team_assignment import get_team_assignment

class TestTeamAssignment(unittest.TestCase):
    """Test cases for team assignment functionality"""
    
    def test_network_team_assignment(self):
        """Test network team assignment"""
        test_texts = [
            "Cannot connect to WiFi network",
            "Internet is down in the office",
            "VPN connection issues from home",
            "Router is not working properly",
            "Need help with DNS configuration"
        ]
        
        for text in test_texts:
            with self.subTest(text=text):
                team = get_team_assignment(text)
                self.assertEqual(team, "network")
    
    def test_hardware_team_assignment(self):
        """Test hardware team assignment"""
        test_texts = [
            "My laptop screen is broken",
            "Need a replacement keyboard",
            "Computer won't turn on",
            "Printer is not printing documents",
            "Battery is not charging on my laptop"
        ]
        
        for text in test_texts:
            with self.subTest(text=text):
                team = get_team_assignment(text)
                self.assertEqual(team, "hardware")
    
    def test_software_team_assignment(self):
        """Test software team assignment"""
        test_texts = [
            "Microsoft Word keeps crashing",
            "Need to install new software",
            "Application is showing error message",
            "Windows updates not working",
            "Excel spreadsheet is corrupted"
        ]
        
        for text in test_texts:
            with self.subTest(text=text):
                team = get_team_assignment(text)
                self.assertEqual(team, "software")
    
    def test_security_team_assignment(self):
        """Test security team assignment"""
        test_texts = [
            "Need to reset my password",
            "Suspicious emails in my inbox",
            "Possible virus on my computer",
            "Account got locked after multiple login attempts",
            "Need access to restricted database"
        ]
        
        for text in test_texts:
            with self.subTest(text=text):
                team = get_team_assignment(text)
                self.assertEqual(team, "security")
    
    def test_default_team_assignment(self):
        """Test default team assignment when no clear match"""
        test_texts = [
            "Not sure what's wrong",
            "Need help with something",
            "Having issues with my work",
            "Everything is slow today"
        ]
        
        for text in test_texts:
            with self.subTest(text=text):
                team = get_team_assignment(text)
                self.assertEqual(team, "software")  # Default is software
    
    def test_mixed_keywords(self):
        """Test when text contains keywords from multiple teams"""
        # This text has both network and security keywords, but more security keywords
        text = "My password isn't working for the VPN connection. I think my account might be compromised."
        team = get_team_assignment(text)
        self.assertEqual(team, "security")
        
        # This text has both hardware and software keywords, but more hardware keywords
        text = "My laptop keyboard isn't working properly and I can't type in any applications."
        team = get_team_assignment(text)
        self.assertEqual(team, "hardware")


if __name__ == '__main__':
    unittest.main()