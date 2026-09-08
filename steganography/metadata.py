"""
Metadata Handler - File Metadata Management
Stores and retrieves file information for steganographic images
"""

import json
import struct
from datetime import datetime


class Metadata:
    """
    Manages metadata for hidden files
    """
    
    def __init__(self, filename, file_size, file_hash, compressed=False):
        """
        Initialize metadata
        
        Args:
            filename (str): Original filename
            file_size (int): Original file size
            file_hash (str): SHA-256 hash of file
            compressed (bool): Whether file is compressed
        """
        self.filename = filename
        self.file_size = file_size
        self.file_hash = file_hash
        self.compressed = compressed
        self.timestamp = datetime.now().isoformat()
        self.version = 1
    
    def to_dict(self):
        """
        Convert metadata to dictionary
        
        Returns:
            dict: Metadata dictionary
        """
        return {
            'version': self.version,
            'filename': self.filename,
            'file_size': self.file_size,
            'file_hash': self.file_hash,
            'compressed': self.compressed,
            'timestamp': self.timestamp
        }
    
    def to_json(self):
        """
        Convert metadata to JSON bytes
        
        Returns:
            bytes: JSON encoded metadata
        """
        return json.dumps(self.to_dict()).encode('utf-8')
    
    @staticmethod
    def from_json(json_bytes):
        """
        Create metadata from JSON bytes
        
        Args:
            json_bytes (bytes): JSON encoded metadata
            
        Returns:
            Metadata: Metadata object
        """
        data = json.loads(json_bytes.decode('utf-8'))
        
        meta = Metadata(
            filename=data['filename'],
            file_size=data['file_size'],
            file_hash=data['file_hash'],
            compressed=data.get('compressed', False)
        )
        
        meta.timestamp = data.get('timestamp', meta.timestamp)
        meta.version = data.get('version', 1)
        
        return meta
    
    def to_bytes(self):
        """
        Convert metadata to binary format
        Format: [length (4 bytes)] + [JSON data]
        
        Returns:
            bytes: Binary encoded metadata
        """
        json_data = self.to_json()
        length = len(json_data)
        return struct.pack('>I', length) + json_data
    
    @staticmethod
    def from_bytes(data):
        """
        Create metadata from binary format
        
        Args:
            data (bytes): Binary encoded metadata
            
        Returns:
            tuple: (Metadata object, remaining bytes)
        """
        if len(data) < 4:
            raise ValueError("Invalid metadata format")
        
        length = struct.unpack('>I', data[:4])[0]
        
        if len(data) < 4 + length:
            raise ValueError("Incomplete metadata")
        
        json_data = data[4:4 + length]
        metadata = Metadata.from_json(json_data)
        
        return metadata, data[4 + length:]
    
    def __repr__(self):
        """String representation"""
        return (
            f"Metadata(filename='{self.filename}', "
            f"size={self.file_size}, compressed={self.compressed})"
        )
