# QUICK_START.md

## Quick Start Guide

### Installation (2 minutes)

```bash
# Clone repository
git clone https://github.com/vasundhara261/secure-file-sharing-system.git
cd secure-file-sharing-system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Usage

#### Option 1: Command Line Interface (Fastest)

**Hide a file:**
```bash
python main.py hide -i cover.png -f secret.pdf -o output.png -p "MyPassword123!"
```

**Extract a file:**
```bash
python main.py extract -i output.png -o recovered.pdf -p "MyPassword123!"
```

**Check image capacity:**
```bash
python main.py info -i cover.png
```

#### Option 2: Web Interface (Most User-Friendly)

```bash
python app.py
# Open http://localhost:5000 in browser
```

#### Option 3: Python API (Most Flexible)

```python
from secure_sharing import SecureFileSharingSystem

system = SecureFileSharingSystem()

# Hide file
result = system.hide_file(
    cover_image_path='cover.png',
    secret_file_path='secret.txt',
    output_image_path='output.png',
    password='SecurePassword123!'
)

if result['success']:
    print(f"Hidden! Capacity used: {result['used_capacity_percent']:.2f}%")

# Extract file
result = system.extract_file(
    stego_image_path='output.png',
    output_file_path='recovered.txt',
    password='SecurePassword123!'
)

if result['success']:
    print(f"Extracted! File: {result['filename']}")
```

### Common Commands

```bash
# Hide with compression (default)
python main.py hide -i img.png -f file.txt -o out.png -p "pass"

# Hide without compression
python main.py hide -i img.png -f file.txt -o out.png -p "pass" --compress false

# Use more bit planes (higher capacity, less safe)
python main.py hide -i img.png -f file.txt -o out.png -p "pass" -b 3

# Extract with specific bit planes
python main.py extract -i out.png -o file.txt -p "pass" -b 3

# Check password strength
python main.py checkpass
```

### Tips & Tricks

1. **Best Images**: Use high-resolution, natural photos (no filters)
2. **Strong Passwords**: Mix uppercase, lowercase, numbers, symbols
3. **Test Extraction**: Always verify extraction before sharing
4. **Large Files**: Use compression flag to save space
5. **Multiple Files**: Hide each file in a separate image

### Troubleshooting

**"File too large" error**
- Use a larger image
- Enable compression: `-c`
- Check capacity: `python main.py info -i image.png`

**"Hash verification failed" error**
- Wrong password
- Image corrupted
- Wrong bit planes setting

**"Image not found" error**
- Check file path
- Use absolute paths if relative doesn't work

### Performance Tips

- Compression reduces file size by ~70% for text
- LSB (1 bit plane) is faster and safest
- PNG is lossless, JPG may cause extraction issues
- SSD is faster for large files

### Next Steps

1. Read [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
2. Check [examples/](examples/) for more use cases
3. Review [README.md](README.md) for full documentation
4. Run tests: `pytest tests/`

### Support

Issues? Check:
- [GitHub Issues](https://github.com/vasundhara261/secure-file-sharing-system/issues)
- [Security Considerations](README.md#security-considerations)
- [API Documentation](README.md#api-documentation)
