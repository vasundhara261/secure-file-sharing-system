"""
Cryptography Module - AES-256 Encryption
Provides secure encryption and decryption using AES-256-CBC
"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os


class AESCipher:
    """
    AES-256 cipher for encrypting and decrypting data
    Uses CBC mode with PKCS7 padding
    """
    
    def __init__(self, key):
        """
        Initialize AES cipher with a 256-bit key
        
        Args:
            key (bytes): 32-byte encryption key
        """
        if len(key) != 32:
            raise ValueError("Key must be 32 bytes for AES-256")
        self.key = key
        self.backend = default_backend()
    
    def encrypt(self, plaintext):
        """
        Encrypt plaintext using AES-256-CBC
        
        Args:
            plaintext (bytes): Data to encrypt
            
        Returns:
            tuple: (ciphertext, iv) - both as bytes
        """
        # Generate random IV
        iv = os.urandom(16)
        
        # Create cipher
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv),
            backend=self.backend
        )
        encryptor = cipher.encryptor()
        
        # Add PKCS7 padding
        plaintext = self._add_padding(plaintext)
        
        # Encrypt
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()
        
        return ciphertext, iv
    
    def decrypt(self, ciphertext, iv):
        """
        Decrypt ciphertext using AES-256-CBC
        
        Args:
            ciphertext (bytes): Data to decrypt
            iv (bytes): Initialization vector (16 bytes)
            
        Returns:
            bytes: Decrypted plaintext
        """
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv),
            backend=self.backend
        )
        decryptor = cipher.decryptor()
        
        # Decrypt
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Remove PKCS7 padding
        plaintext = self._remove_padding(plaintext)
        
        return plaintext
    
    @staticmethod
    def _add_padding(data):
        """Add PKCS7 padding"""
        padding_length = 16 - (len(data) % 16)
        padding = bytes([padding_length] * padding_length)
        return data + padding
    
    @staticmethod
    def _remove_padding(data):
        """Remove PKCS7 padding"""
        padding_length = data[-1]
        return data[:-padding_length]
