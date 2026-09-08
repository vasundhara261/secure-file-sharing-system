"""
LSB Encoder - Least Significant Bit Steganography
Hides data in image using LSB encoding technique
"""

import numpy as np
from .image_handler import ImageHandler


class LSBEncoder:
    """
    Encodes data into image using Least Significant Bit technique
    """
    
    def __init__(self, image_path):
        """
        Initialize LSB encoder
        
        Args:
            image_path (str): Path to cover image
        """
        self.image_handler = ImageHandler(image_path)
        self.pixels = self.image_handler.get_pixels_array()
    
    def encode(self, data, output_path, bit_planes=1):
        """
        Encode data into image
        
        Args:
            data (bytes): Data to hide
            output_path (str): Path to save output image
            bit_planes (int): Number of LSBs to use (1-8)
            
        Returns:
            bool: Success status
        """
        if bit_planes < 1 or bit_planes > 8:
            raise ValueError("bit_planes must be between 1 and 8")
        
        # Check capacity
        max_bytes = self.image_handler.get_capacity(bit_planes)
        data_length = len(data)
        
        if data_length > max_bytes - 4:  # 4 bytes for length header
            raise ValueError(
                f"Data too large: {data_length} bytes, "
                f"max: {max_bytes - 4} bytes"
            )
        
        # Flatten pixels
        pixels = self.pixels.flatten()
        
        # Create data packet: [length (4 bytes)] + [data]
        length_bytes = len(data).to_bytes(4, byteorder='big')
        full_data = length_bytes + data
        
        # Convert data to binary
        binary_data = ''.join(format(byte, '08b') for byte in full_data)
        
        # Create mask for LSBs
        mask = (0xFF << (8 - bit_planes)) & 0xFF
        lsb_mask = 0xFF ^ mask
        
        # Embed data
        bit_index = 0
        for i in range(len(pixels)):
            if bit_index >= len(binary_data):
                break
            
            pixel_value = pixels[i]
            
            # Extract bits to embed
            bits_to_embed = binary_data[bit_index:bit_index + bit_planes]
            if len(bits_to_embed) < bit_planes:
                bits_to_embed += '0' * (bit_planes - len(bits_to_embed))
            
            embedded_bits = int(bits_to_embed, 2)
            
            # Clear LSBs and embed new bits
            pixels[i] = (pixel_value & mask) | embedded_bits
            
            bit_index += bit_planes
        
        # Reshape and save
        output_pixels = pixels.reshape(self.pixels.shape)
        self.image_handler.set_pixels_array(output_pixels)
        self.image_handler.save(output_path)
        
        return True
    
    def get_embedding_info(self, data_size, bit_planes=1):
        """
        Get information about embedding
        
        Args:
            data_size (int): Size of data to embed
            bit_planes (int): Number of LSBs to use
            
        Returns:
            dict: Embedding statistics
        """
        capacity = self.image_handler.get_capacity(bit_planes)
        
        return {
            'image_size': self.pixels.shape,
            'total_pixels': self.image_handler.width * self.image_handler.height,
            'data_size_bytes': data_size,
            'capacity_bytes': capacity,
            'usage_percent': (data_size / capacity) * 100,
            'bit_planes': bit_planes,
            'bits_per_pixel': 3 * bit_planes  # RGB channels
        }


class LSBDecoder:
    """
    Decodes data from image using LSB technique
    """
    
    def __init__(self, image_path):
        """
        Initialize LSB decoder
        
        Args:
            image_path (str): Path to steganographic image
        """
        self.image_handler = ImageHandler(image_path)
        self.pixels = self.image_handler.get_pixels_array()
    
    def decode(self, bit_planes=1):
        """
        Decode data from image
        
        Args:
            bit_planes (int): Number of LSBs used in encoding (1-8)
            
        Returns:
            bytes: Extracted data
        """
        if bit_planes < 1 or bit_planes > 8:
            raise ValueError("bit_planes must be between 1 and 8")
        
        # Flatten pixels
        pixels = self.pixels.flatten()
        
        # Create mask for LSBs
        lsb_mask = (1 << bit_planes) - 1
        
        # Extract binary data
        binary_data = ''
        
        # First extract length (4 bytes = 32 bits)
        for i in range(0, 32, bit_planes):
            pixel_value = pixels[i // bit_planes]
            lsb_bits = pixel_value & lsb_mask
            binary_data += format(lsb_bits, f'0{bit_planes}b')
        
        # Get data length
        data_length = int(binary_data[:32], 2)
        
        # Extract remaining data
        required_bits = (data_length * 8) + 32
        
        binary_data = ''
        for i in range(len(pixels)):
            if len(binary_data) >= required_bits:
                break
            
            pixel_value = pixels[i]
            lsb_bits = pixel_value & lsb_mask
            binary_data += format(lsb_bits, f'0{bit_planes}b')
        
        # Convert binary to bytes, skip length header
        extracted_data = bytearray()
        for i in range(32, required_bits, 8):
            byte_str = binary_data[i:i+8]
            if len(byte_str) == 8:
                extracted_data.append(int(byte_str, 2))
        
        return bytes(extracted_data[:data_length])
