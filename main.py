"""
CLI Interface - Command-line interface for secure file sharing
Provides user-friendly commands for hide and extract operations
"""

import click
from secure_sharing import SecureFileSharingSystem
from core.utils import Utils
from cryptography_module import KeyDerivation
import sys


@click.group()
def cli():
    """
    Secure File Sharing System - Hide and extract files in images
    """
    pass


@cli.command()
@click.option('-i', '--image', 'cover_image', required=True, help='Cover image path')
@click.option('-f', '--file', 'secret_file', required=True, help='Secret file to hide')
@click.option('-o', '--output', 'output_image', required=True, help='Output image path')
@click.option('-p', '--password', required=True, help='Encryption password')
@click.option('-c', '--compress', is_flag=True, default=True, help='Compress file')
@click.option('-b', '--bit-planes', type=int, default=1, help='Bit planes (1-8)')
def hide(cover_image, secret_file, output_image, password, compress, bit_planes):
    """
    Hide a secret file inside a cover image
    """
    # Validate password strength
    is_valid, feedback = Utils.validate_password(password)
    if not is_valid:
        Utils.print_warning("Weak password detected:")
        for msg in feedback:
            click.echo(f"  - {msg}")
    
    # Perform hiding
    system = SecureFileSharingSystem()
    result = system.hide_file(
        cover_image,
        secret_file,
        output_image,
        password,
        compress=compress,
        bit_planes=bit_planes
    )
    
    if result['success']:
        Utils.print_success(f"File hidden successfully in {result['output_path']}")
        click.echo(f"\nStatistics:")
        click.echo(f"  Original size: {Utils.format_bytes(result['original_size_bytes'])}")
        click.echo(f"  Compressed size: {Utils.format_bytes(result['compressed_size_bytes'])}")
        click.echo(f"  Compression ratio: {result['compression_ratio']:.2%}")
        click.echo(f"  Image capacity used: {result['used_capacity_percent']:.2f}%")
        click.echo(f"  File hash: {result['file_hash'][:16]}...")
    else:
        Utils.print_error(f"Failed to hide file: {result['error']}")
        sys.exit(1)


@cli.command()
@click.option('-i', '--image', 'stego_image', required=True, help='Stego image path')
@click.option('-o', '--output', 'output_file', required=True, help='Output file path')
@click.option('-p', '--password', required=True, help='Decryption password')
@click.option('-b', '--bit-planes', type=int, default=1, help='Bit planes (1-8)')
def extract(stego_image, output_file, password, bit_planes):
    """
    Extract a hidden file from a stego image
    """
    system = SecureFileSharingSystem()
    result = system.extract_file(
        stego_image,
        output_file,
        password,
        bit_planes=bit_planes
    )
    
    if result['success']:
        Utils.print_success(f"File extracted successfully to {result['output_path']}")
        click.echo(f"\nFile Information:")
        click.echo(f"  Original filename: {result['filename']}")
        click.echo(f"  Extracted size: {Utils.format_bytes(result['extracted_size_bytes'])}")
        click.echo(f"  Original size: {Utils.format_bytes(result['original_size_bytes'])}")
        click.echo(f"  Was compressed: {result['was_compressed']}")
        click.echo(f"  File hash: {result['file_hash'][:16]}...")
        click.echo(f"  Timestamp: {result['timestamp']}")
    else:
        Utils.print_error(f"Failed to extract file: {result['error']}")
        sys.exit(1)


@cli.command()
@click.option('-i', '--image', 'image_path', required=True, help='Image path')
def info(image_path):
    """
    Display image capacity and information
    """
    system = SecureFileSharingSystem()
    result = system.get_image_info(image_path)
    
    if 'error' not in result:
        Utils.print_info(f"Image Information: {image_path}")
        click.echo(f"\n  Dimensions: {result['width']}x{result['height']}")
        click.echo(f"  Format: {result['format']}")
        click.echo(f"  File size: {Utils.format_bytes(result['size_bytes'])}")
        click.echo(f"  Hiding capacity: {Utils.format_bytes(result['capacity_bytes'])}")
        click.echo(f"\nNote: Actual capacity depends on compression and bit planes used")
    else:
        Utils.print_error(f"Failed to read image: {result['error']}")
        sys.exit(1)


@cli.command()
@click.option('-p', '--password', required=True, prompt=True, hide_input=True, 
              confirmation_prompt=True, help='Password to check')
def checkpass(password):
    """
    Check password strength and recommendations
    """
    strength = KeyDerivation.verify_key_strength(password)
    
    click.echo(f"\nPassword Strength: {strength['strength']} ({strength['score']}/5)")
    click.echo(f"\nRequirements:")
    reqs = strength['requirements']
    click.echo(f"  ✓ Length >= 16 chars: {'Yes' if reqs['length'] else 'No'}")
    click.echo(f"  ✓ Uppercase: {'Yes' if reqs['has_uppercase'] else 'No'}")
    click.echo(f"  ✓ Lowercase: {'Yes' if reqs['has_lowercase'] else 'No'}")
    click.echo(f"  ✓ Digits: {'Yes' if reqs['has_digits'] else 'No'}")
    click.echo(f"  ✓ Special chars: {'Yes' if reqs['has_special'] else 'No'}")


if __name__ == '__main__':
    cli()
