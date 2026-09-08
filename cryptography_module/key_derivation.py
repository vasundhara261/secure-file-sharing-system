"""
Key Derivation Module - Secure Password-based Key Generation
Uses PBKDF2 to derive cryptographic keys from passwords
"""

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from cryptography.hazmat.backends import default_backend
import os


class KeyDerivation:
    """
    Derives cryptographic keys from passwords using PBKDF2
    """
    
    # Security parameters
    ITERATIONS = 100000
    ALGORITHM = hashes.SHA256()
    KEY_LENGTH = 32  # 256 bits for AES-256
    
    @staticmethod
    def derive_key(password, salt=None):
        """
        Derive a 256-bit encryption key from a password
        
        Args:
            password (str): User password
            salt (bytes): Random salt (generates if None)
            
        Returns:
            tuple: (key, salt) - both as bytes
        """
        if isinstance(password, str):
            password = password.encode('utf-8')
        
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2(
            algorithm=KeyDerivation.ALGORITHM,
            length=KeyDerivation.KEY_LENGTH,
            salt=salt,
            iterations=KeyDerivation.ITERATIONS,
            backend=default_backend()
        )
        
        key = kdf.derive(password)
        return key, salt
    
    @staticmethod
    def generate_salt(length=16):
        """
        Generate a random salt
        
        Args:
            length (int): Salt length in bytes (default 16)
            
        Returns:
            bytes: Random salt
        """
        return os.urandom(length)
    
    @staticmethod
    def verify_key_strength(password):
        """
        Check password strength (recommendation only)
        
        Args:
            password (str): Password to check
            
        Returns:
            dict: Strength assessment
        """
        requirements = {
            'length': len(password) >= 16,
            'has_uppercase': any(c.isupper() for c in password),
            'has_lowercase': any(c.islower() for c in password),
            'has_digits': any(c.isdigit() for c in password),
            'has_special': any(not c.isalnum() for c in password)
        }
        
        score = sum(requirements.values())
        strength_levels = {
            0: 'Very Weak',
            1: 'Weak',
            2: 'Fair',
            3: 'Good',
            4: 'Strong',
            5: 'Very Strong'
        }
        
        return {
            'strength': strength_levels.get(score, 'Unknown'),
            'score': score,
            'requirements': requirements
        }
