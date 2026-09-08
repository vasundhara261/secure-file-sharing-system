"""
Test Suite - Unit and integration tests
"""

import pytest
import os
import tempfile
from steganography import LSBEncoder, LSBDecoder
from cryptography_module import AESCipher, KeyDerivation, HashUtils
from core.file_operations import FileOperations
from core.compression import CompressionHandler
from secure_sharing import SecureFileSharingSystem


class TestCryptography:
    """
    Test cryptography module
    """
    
    def test_aes_encryption_decryption(self):
        """Test AES encrypt/decrypt round trip"""
        key = b'0' * 32
        cipher = AESCipher(key)
        plaintext = b'Hello, World!'
        
        encrypted, iv = cipher.encrypt(plaintext)
        decrypted = cipher.decrypt(encrypted, iv)
        
        assert decrypted == plaintext
    
    def test_key_derivation(self):
        """Test PBKDF2 key derivation"""
        password = "TestPassword123!"
        key1, salt1 = KeyDerivation.derive_key(password)
        key2, salt2 = KeyDerivation.derive_key(password, salt=salt1)
        
        assert len(key1) == 32
        assert key1 == key2
    
    def test_hash_computation(self):
        """Test SHA-256 hashing"""
        data = b'Test data'
        hash1 = HashUtils.compute_hash(data)
        hash2 = HashUtils.compute_hash(data)
        
        assert hash1 == hash2
        assert len(hash1) == 64  # SHA-256 hex string


class TestFileOperations:
    """
    Test file operations
    """
    
    def test_file_read_write(self):
        """Test file read and write"""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        
        test_data = b'Test file content'
        FileOperations.write_file(temp_path, test_data)
        read_data = FileOperations.read_file(temp_path)
        
        assert read_data == test_data
        os.unlink(temp_path)
    
    def test_file_info(self):
        """Test file info retrieval"""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
            f.write(b'test')
        
        info = FileOperations.get_file_info(temp_path)
        
        assert info['exists']
        assert info['is_file']
        assert info['size_bytes'] == 4
        os.unlink(temp_path)


class TestCompression:
    """
    Test compression module
    """
    
    def test_compress_decompress(self):
        """Test compression round trip"""
        data = b'A' * 1000
        compressed = CompressionHandler.compress(data)
        decompressed = CompressionHandler.decompress(compressed)
        
        assert decompressed == data
        assert len(compressed) < len(data)
    
    def test_compression_ratio(self):
        """Test compression ratio calculation"""
        data = b'A' * 1000
        compressed = CompressionHandler.compress(data)
        ratio = CompressionHandler.get_compression_ratio(
            len(data), len(compressed)
        )
        
        assert 0 < ratio < 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
