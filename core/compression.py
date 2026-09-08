"""
Compression Module - Data compression utilities
Provides zlib compression for file size reduction
"""

import zlib


class CompressionHandler:
    """
    Handles data compression and decompression
    """
    
    COMPRESSION_LEVEL = 9  # Maximum compression
    
    @staticmethod
    def compress(data):
        """
        Compress data using zlib
        
        Args:
            data (bytes): Data to compress
            
        Returns:
            bytes: Compressed data
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        return zlib.compress(data, CompressionHandler.COMPRESSION_LEVEL)
    
    @staticmethod
    def decompress(compressed_data):
        """
        Decompress zlib compressed data
        
        Args:
            compressed_data (bytes): Compressed data
            
        Returns:
            bytes: Decompressed data
        """
        try:
            return zlib.decompress(compressed_data)
        except zlib.error as e:
            raise ValueError(f"Decompression failed: {e}")
    
    @staticmethod
    def get_compression_ratio(original_size, compressed_size):
        """
        Calculate compression ratio
        
        Args:
            original_size (int): Original data size
            compressed_size (int): Compressed data size
            
        Returns:
            float: Compression ratio (0-1, lower is better)
        """
        if original_size == 0:
            return 0.0
        
        return compressed_size / original_size
