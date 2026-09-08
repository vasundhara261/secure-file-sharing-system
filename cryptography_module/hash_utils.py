"""
Hash Utilities - SHA-256 Hashing
Provides secure hashing for integrity verification
"""

import hashlib


class HashUtils:
    """
    Utilities for SHA-256 hashing and verification
    """
    
    @staticmethod
    def compute_hash(data):
        """
        Compute SHA-256 hash of data
        
        Args:
            data (bytes): Data to hash
            
        Returns:
            str: Hexadecimal hash string
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        return hashlib.sha256(data).hexdigest()
    
    @staticmethod
    def compute_file_hash(file_path):
        """
        Compute SHA-256 hash of a file
        
        Args:
            file_path (str): Path to file
            
        Returns:
            str: Hexadecimal hash string
        """
        sha256_hash = hashlib.sha256()
        
        with open(file_path, 'rb') as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        return sha256_hash.hexdigest()
    
    @staticmethod
    def verify_hash(data, expected_hash):
        """
        Verify data against expected hash
        
        Args:
            data (bytes): Data to verify
            expected_hash (str): Expected hash value
            
        Returns:
            bool: True if hash matches
        """
        computed = HashUtils.compute_hash(data)
        return computed == expected_hash
    
    @staticmethod
    def verify_file_hash(file_path, expected_hash):
        """
        Verify file against expected hash
        
        Args:
            file_path (str): Path to file
            expected_hash (str): Expected hash value
            
        Returns:
            bool: True if hash matches
        """
        computed = HashUtils.compute_file_hash(file_path)
        return computed == expected_hash
