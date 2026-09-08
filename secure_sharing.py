"""
Main Orchestrator - High-level API for secure file sharing
Combines steganography and cryptography for complete workflow
"""

import os
from steganography import LSBEncoder, LSBDecoder
from cryptography_module import AESCipher, KeyDerivation, HashUtils
from steganography.metadata import Metadata
from core.file_operations import FileOperations
from core.compression import CompressionHandler


class SecureFileSharingSystem:
    """
    Main orchestrator for secure file sharing
    Handles complete hide and extract workflows
    """
    
    def __init__(self):
        """
        Initialize the secure file sharing system
        """
        self.file_ops = FileOperations()
    
    def hide_file(
        self,
        cover_image_path,
        secret_file_path,
        output_image_path,
        password,
        compress=True,
        bit_planes=1
    ):
        """
        Hide a secret file inside a cover image
        
        Args:
            cover_image_path (str): Path to cover image
            secret_file_path (str): Path to secret file
            output_image_path (str): Path to save stego image
            password (str): Encryption password
            compress (bool): Whether to compress data
            bit_planes (int): Number of bit planes to use (1-8)
            
        Returns:
            dict: Operation result with statistics
        """
        try:
            # Read secret file
            secret_data = FileOperations.read_file(secret_file_path)
            original_size = len(secret_data)
            
            # Compress if requested
            if compress:
                secret_data = CompressionHandler.compress(secret_data)
                compressed_size = len(secret_data)
            else:
                compressed_size = original_size
            
            # Calculate file hash
            file_hash = HashUtils.compute_hash(secret_data)
            
            # Create metadata
            filename = os.path.basename(secret_file_path)
            metadata = Metadata(
                filename=filename,
                file_size=original_size,
                file_hash=file_hash,
                compressed=compress
            )
            
            # Derive encryption key
            key, salt = KeyDerivation.derive_key(password)
            
            # Encrypt data
            cipher = AESCipher(key)
            encrypted_data, iv = cipher.encrypt(secret_data)
            
            # Create payload: [salt (16)] + [iv (16)] + [metadata] + [encrypted data]
            metadata_bytes = metadata.to_bytes()
            payload = salt + iv + metadata_bytes + encrypted_data
            
            # Embed in image
            encoder = LSBEncoder(cover_image_path)
            encoder.encode(payload, output_image_path, bit_planes=bit_planes)
            
            # Get statistics
            output_size = os.path.getsize(output_image_path)
            image_info = encoder.image_handler.get_image_info()
            
            return {
                'success': True,
                'output_path': output_image_path,
                'original_size_bytes': original_size,
                'compressed_size_bytes': compressed_size,
                'compression_ratio': compressed_size / original_size if original_size > 0 else 0,
                'encrypted_size_bytes': len(encrypted_data),
                'output_image_size': output_size,
                'image_capacity': image_info['capacity_bytes'],
                'used_capacity_percent': (len(payload) / image_info['capacity_bytes']) * 100,
                'file_hash': file_hash,
                'bit_planes': bit_planes
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def extract_file(
        self,
        stego_image_path,
        output_file_path,
        password,
        bit_planes=1
    ):
        """
        Extract a hidden file from a stego image
        
        Args:
            stego_image_path (str): Path to stego image
            output_file_path (str): Path to save extracted file
            password (str): Decryption password
            bit_planes (int): Number of bit planes used (1-8)
            
        Returns:
            dict: Operation result with statistics
        """
        try:
            # Decode from image
            decoder = LSBDecoder(stego_image_path)
            payload = decoder.decode(bit_planes=bit_planes)
            
            # Extract components
            salt = payload[:16]
            iv = payload[16:32]
            
            # Parse metadata
            metadata, remaining = Metadata.from_bytes(payload[32:])
            encrypted_data = remaining
            
            # Derive decryption key
            key, _ = KeyDerivation.derive_key(password, salt=salt)
            
            # Decrypt data
            cipher = AESCipher(key)
            decrypted_data = cipher.decrypt(encrypted_data, iv)
            
            # Decompress if needed
            if metadata.compressed:
                decrypted_data = CompressionHandler.decompress(decrypted_data)
            
            # Verify hash
            calculated_hash = HashUtils.compute_hash(decrypted_data)
            if calculated_hash != metadata.file_hash:
                return {
                    'success': False,
                    'error': 'Hash verification failed - file may be corrupted or password incorrect'
                }
            
            # Save file
            FileOperations.write_file(output_file_path, decrypted_data)
            
            return {
                'success': True,
                'output_path': output_file_path,
                'filename': metadata.filename,
                'extracted_size_bytes': len(decrypted_data),
                'original_size_bytes': metadata.file_size,
                'was_compressed': metadata.compressed,
                'file_hash': metadata.file_hash,
                'timestamp': metadata.timestamp
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_image_info(self, image_path):
        """
        Get information about image capacity
        
        Args:
            image_path (str): Path to image
            
        Returns:
            dict: Image information
        """
        from steganography.image_handler import ImageHandler
        
        try:
            handler = ImageHandler(image_path)
            return handler.get_image_info()
        except Exception as e:
            return {'error': str(e)}
