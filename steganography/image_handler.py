"""
Image Handler - Image Processing Utilities
Handles image loading, saving, and pixel manipulation
"""

from PIL import Image
import numpy as np
import os


class ImageHandler:
    """
    Handles image operations for steganography
    """
    
    SUPPORTED_FORMATS = {'PNG', 'JPG', 'JPEG', 'BMP'}
    
    def __init__(self, image_path):
        """
        Initialize image handler
        
        Args:
            image_path (str): Path to image file
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        self.image_path = image_path
        self.image = Image.open(image_path)
        self.original_format = self.image.format
        
        # Convert to RGB if needed
        if self.image.mode != 'RGB':
            self.image = self.image.convert('RGB')
        
        self.width, self.height = self.image.size
    
    def get_pixels_array(self):
        """
        Get image as numpy array
        
        Returns:
            np.ndarray: Pixel array (height, width, 3)
        """
        return np.array(self.image)
    
    def set_pixels_array(self, pixels_array):
        """
        Set image from numpy array
        
        Args:
            pixels_array (np.ndarray): Pixel array
        """
        self.image = Image.fromarray(pixels_array.astype('uint8'), 'RGB')
    
    def save(self, output_path, quality=95):
        """
        Save image to file
        
        Args:
            output_path (str): Path to save image
            quality (int): JPEG quality (1-100)
        """
        if output_path.lower().endswith(('.jpg', '.jpeg')):
            self.image.save(output_path, quality=quality)
        else:
            self.image.save(output_path)
    
    def get_capacity(self, bits_per_pixel=1):
        """
        Calculate maximum bytes that can be hidden
        
        Args:
            bits_per_pixel (int): Bits used per pixel (1 or more)
            
        Returns:
            int: Maximum bytes that can be hidden
        """
        # Each pixel has 3 channels (RGB)
        total_bits = self.width * self.height * 3 * bits_per_pixel
        return total_bits // 8
    
    def is_valid_format(self):
        """
        Check if image format is supported
        
        Returns:
            bool: True if supported
        """
        return self.original_format.upper() in self.SUPPORTED_FORMATS
    
    def get_image_info(self):
        """
        Get image information
        
        Returns:
            dict: Image metadata
        """
        return {
            'path': self.image_path,
            'width': self.width,
            'height': self.height,
            'format': self.original_format,
            'mode': self.image.mode,
            'size_bytes': os.path.getsize(self.image_path),
            'capacity_bytes': self.get_capacity()
        }
