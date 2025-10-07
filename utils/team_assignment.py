"""
Team assignment utilities for the Smart IT Ticket Prioritizer.

This module provides functions for assigning tickets to relevant teams
based on the ticket content.
"""
import re
from collections import Counter

# Define team keywords
TEAM_KEYWORDS = {
    'network': [
        'network', 'wifi', 'connection', 'internet', 'router', 'switch', 'lan', 'wan', 
        'ethernet', 'connectivity', 'vpn', 'dns', 'ip', 'subnet', 'firewall', 'ping'
    ],
    'hardware': [
        'hardware', 'computer', 'laptop', 'desktop', 'monitor', 'keyboard', 'mouse', 
        'printer', 'scanner', 'device', 'broken', 'physical', 'motherboard', 'cpu', 
        'ram', 'memory', 'hard drive', 'ssd', 'usb', 'battery', 'power', 'charger'
    ],
    'software': [
        'software', 'application', 'program', 'install', 'update', 'upgrade', 'bug', 
        'error', 'crash', 'freeze', 'slow', 'performance', 'windows', 'mac', 'office', 
        'excel', 'word', 'outlook', 'browser', 'chrome', 'firefox', 'edge'
    ],
    'security': [
        'security', 'password', 'access', 'permission', 'virus', 'malware', 'spam', 
        'phishing', 'breach', 'unauthorized', 'login', 'authentication', 'encryption', 
        'secure', 'vulnerability', 'threat', 'attack', 'hack'
    ]
}

def get_team_assignment(text):
    """
    Assign a ticket to a team based on keyword matching.
    
    Args:
        text (str): The preprocessed text of the ticket
        
    Returns:
        str: Team assignment (network, hardware, software, or security)
    """
    text = text.lower()
    
    # Count occurrences of keywords for each team
    team_scores = {}
    for team, keywords in TEAM_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            # Add score based on keyword matches
            score += len(re.findall(r'\b' + re.escape(keyword) + r'\b', text))
        team_scores[team] = score
    
    # Find team with highest score
    max_score = max(team_scores.values())
    
    # If there's a tie or no matches, assign to 'software' (default team)
    if max_score == 0 or list(team_scores.values()).count(max_score) > 1:
        return 'software'
    
    # Return the team with the highest score
    return max(team_scores, key=team_scores.get)