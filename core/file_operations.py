"""
File Operations Module - High-level file handling
Manages reading, writing, and validation of files
"""

import os
from pathlib import Path


class FileOperations:
    """
    Handles file I/O operations
    """
    
    MAX_FILE_SIZE = 500 * 1024 * 1024  # 500 MB
    
    @staticmethod
    def read_file(file_path):
        """
        Read file contents
        
        Args:
            file_path (str): Path to file
            
        Returns:
            bytes: File contents
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_size = os.path.getsize(file_path)
        if file_size > FileOperations.MAX_FILE_SIZE:
            raise ValueError(f"File too large: {file_size} bytes")
        
        with open(file_path, 'rb') as f:
            return f.read()
    
    @staticmethod
    def write_file(file_path, data):
        """
        Write data to file
        
        Args:
            file_path (str): Path to save file
            data (bytes): Data to write
        """
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        
        with open(file_path, 'wb') as f:
            f.write(data)
    
    @staticmethod
    def get_file_info(file_path):
        """
        Get file information
        
        Args:
            file_path (str): Path to file
            
        Returns:
            dict: File metadata
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        stat_info = os.stat(file_path)
        
        return {
            'path': file_path,
            'name': os.path.basename(file_path),
            'size_bytes': stat_info.st_size,
            'modified_time': stat_info.st_mtime,
            'is_file': os.path.isfile(file_path),
            'exists': os.path.exists(file_path)
        }
    
    @staticmethod
    def validate_file_path(file_path, must_exist=True):
        """
        Validate file path
        
        Args:
            file_path (str): Path to validate
            must_exist (bool): Whether file must exist
            
        Returns:
            bool: True if valid
        """
        if must_exist and not os.path.exists(file_path):
            return False
        
        try:
            Path(file_path).resolve()
            return True
        except (OSError, ValueError):
            return False
    
    @staticmethod
    def file_exists(file_path):
        """
        Check if file exists
        
        Args:
            file_path (str): Path to check
            
        Returns:
            bool: True if exists
        """
        return os.path.exists(file_path) and os.path.isfile(file_path)
