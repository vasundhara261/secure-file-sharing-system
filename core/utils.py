"""
Utilities Module - General utility functions
Provides helper functions for common operations
"""

import os
import sys
from colorama import Fore, Style


class Utils:
    """
    Utility functions for the system
    """
    
    @staticmethod
    def format_bytes(size_bytes):
        """
        Format bytes to human-readable format
        
        Args:
            size_bytes (int): Size in bytes
            
        Returns:
            str: Formatted size string
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        
        return f"{size_bytes:.2f} PB"
    
    @staticmethod
    def print_success(message):
        """
        Print success message in green
        
        Args:
            message (str): Message to print
        """
        print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")
    
    @staticmethod
    def print_error(message):
        """
        Print error message in red
        
        Args:
            message (str): Message to print
        """
        print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")
    
    @staticmethod
    def print_warning(message):
        """
        Print warning message in yellow
        
        Args:
            message (str): Message to print
        """
        print(f"{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}")
    
    @staticmethod
    def print_info(message):
        """
        Print info message in blue
        
        Args:
            message (str): Message to print
        """
        print(f"{Fore.CYAN}ℹ {message}{Style.RESET_ALL}")
    
    @staticmethod
    def clear_screen():
        """
        Clear terminal screen
        """
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def validate_password(password):
        """
        Validate password strength
        
        Args:
            password (str): Password to validate
            
        Returns:
            tuple: (is_valid, feedback)
        """
        feedback = []
        
        if len(password) < 8:
            feedback.append("Password must be at least 8 characters")
        
        if len(password) < 16:
            feedback.append("Consider using 16+ characters for better security")
        
        if not any(c.isupper() for c in password):
            feedback.append("Add uppercase letters")
        
        if not any(c.islower() for c in password):
            feedback.append("Add lowercase letters")
        
        if not any(c.isdigit() for c in password):
            feedback.append("Add digits")
        
        if not any(not c.isalnum() for c in password):
            feedback.append("Add special characters")
        
        is_valid = len(password) >= 8
        return is_valid, feedback
