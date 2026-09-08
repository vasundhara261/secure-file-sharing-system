"""
Core Module - Central file operations and utilities
Exports main functionality classes
"""

from .file_operations import FileOperations
from .compression import CompressionHandler
from .utils import Utils

__all__ = [
    'FileOperations',
    'CompressionHandler',
    'Utils'
]
