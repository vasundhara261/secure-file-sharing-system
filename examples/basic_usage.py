"""
Basic Usage Example - Simple demonstration of hide and extract operations
"""

from secure_sharing import SecureFileSharingSystem
from core.utils import Utils


def example_basic_usage():
    """
    Demonstrate basic hide and extract operations
    """
    
    print("\n" + "="*60)
    print("Secure File Sharing System - Basic Usage Example")
    print("="*60 + "\n")
    
    # Initialize system
    system = SecureFileSharingSystem()
    
    # Example paths (you'll need to adjust these)
    cover_image = "examples/sample_image.png"
    secret_file = "examples/secret_document.txt"
    output_image = "examples/output_image.png"
    extracted_file = "examples/recovered_document.txt"
    password = "SecurePassword123!"
    
    print("\n[STEP 1] Hide a secret file in an image")
    print("-" * 60)
    
    result = system.hide_file(
        cover_image=cover_image,
        secret_file_path=secret_file,
        output_image_path=output_image,
        password=password,
        compress=True,
        bit_planes=1
    )
    
    if result['success']:
        Utils.print_success("File hidden successfully!")
        print(f"\nStatistics:")
        print(f"  Output: {result['output_path']}")
        print(f"  Original size: {Utils.format_bytes(result['original_size_bytes'])}")
        print(f"  Compressed size: {Utils.format_bytes(result['compressed_size_bytes'])}")
        print(f"  Compression ratio: {result['compression_ratio']:.2%}")
        print(f"  Image capacity used: {result['used_capacity_percent']:.2f}%")
        print(f"  File hash: {result['file_hash'][:16]}...")
    else:
        Utils.print_error(f"Failed: {result['error']}")
        return
    
    print("\n[STEP 2] Extract the hidden file")
    print("-" * 60)
    
    result = system.extract_file(
        stego_image_path=output_image,
        output_file_path=extracted_file,
        password=password,
        bit_planes=1
    )
    
    if result['success']:
        Utils.print_success("File extracted successfully!")
        print(f"\nFile Information:")
        print(f"  Original filename: {result['filename']}")
        print(f"  Extracted to: {result['output_path']}")
        print(f"  Size: {Utils.format_bytes(result['extracted_size_bytes'])}")
        print(f"  Was compressed: {result['was_compressed']}")
        print(f"  Timestamp: {result['timestamp']}")
    else:
        Utils.print_error(f"Failed: {result['error']}")
    
    print("\n" + "="*60)
    print("Example complete!")
    print("="*60 + "\n")


if __name__ == "__main__":
    example_basic_usage()
