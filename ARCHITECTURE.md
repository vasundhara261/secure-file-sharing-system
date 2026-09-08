# ARCHITECTURE.md

## System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────┐
│           Secure File Sharing System                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐        ┌──────────────┐             │
│  │  CLI Layer   │        │  Web Layer   │             │
│  │  (main.py)   │        │  (app.py)    │             │
│  └──────┬───────┘        └──────┬───────┘             │
│         │                       │                      │
│         └───────────┬───────────┘                      │
│                     │                                   │
│                     ▼                                   │
│         ┌───────────────────────┐                      │
│         │  Orchestrator Layer   │                      │
│         │ (secure_sharing.py)   │                      │
│         └───────────┬───────────┘                      │
│                     │                                   │
│    ┌────────────────┼────────────────┐                 │
│    ▼                ▼                ▼                 │
│┌──────────────┐ ┌───────────────┐ ┌────────────────┐  │
│ Steganography│ │ Cryptography  │ │  Core Ops     │  │
│  (LSB Codec) │ │  (AES-256)    │ │  (File/Comp)  │  │
│              │ │  (PBKDF2)     │ │  (Utils)      │  │
│ ├─ LSBEncode │ │  (SHA-256)    │ │               │  │
│ ├─ LSBDecode │ │               │ │ ├─ FileOps    │  │
│ ├─ ImgHandle │ │ ├─ AESCipher  │ │ ├─ Compress   │  │
│ └─ Metadata  │ │ ├─ KeyDeriv   │ │ └─ Utils      │  │
│              │ │ └─ HashUtils  │ │               │  │
│              │ │               │ │               │  │
└──────────────┘ └───────────────┘ └────────────────┘  │
│                     │                                   │
│                     ▼                                   │
│         ┌───────────────────────┐                      │
│         │   Image File System   │                      │
│         │   (PNG/JPG Input)     │                      │
│         └───────────────────────┘                      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Data Flow: Hide Operation

```
User Input (File + Password)
    ↓
1. Read Secret File
    ↓
2. Optional Compression (Zlib)
    ↓
3. Calculate SHA-256 Hash
    ↓
4. Generate Random Salt (16 bytes)
    ↓
5. Derive Key (PBKDF2: 100k iterations)
    ↓
6. Encrypt with AES-256-CBC (generates IV)
    ↓
7. Create Metadata Packet (JSON + length prefix)
    ↓
8. Combine: [Salt] + [IV] + [Metadata] + [Encrypted Data]
    ↓
9. LSB Encode in Cover Image
    ↓
10. Save Stego Image
    ↓
Output: Stego Image File
```

### Data Flow: Extract Operation

```
User Input (Stego Image + Password)
    ↓
1. LSB Decode from Image
    ↓
2. Extract Salt (16 bytes)
    ↓
3. Extract IV (16 bytes)
    ↓
4. Parse Metadata (JSON from packet)
    ↓
5. Extract Encrypted Data
    ↓
6. Derive Key (PBKDF2 with extracted salt)
    ↓
7. Decrypt with AES-256-CBC
    ↓
8. Verify SHA-256 Hash
    ↓
9. Optional Decompression
    ↓
10. Save Extracted File
    ↓
Output: Recovered File
```

## Module Details

### Steganography Module

**Purpose**: Hide and extract data from images using LSB encoding

**Key Classes**:
- `LSBEncoder`: Embeds data into image LSBs
- `LSBDecoder`: Extracts data from image LSBs
- `ImageHandler`: Image I/O and manipulation
- `Metadata`: File metadata (name, size, hash, timestamp)

**Key Algorithms**:
- LSB (Least Significant Bit) encoding
- Configurable bit planes (1-8)
- PNG/JPG format support
- Capacity calculation

### Cryptography Module

**Purpose**: Encrypt/decrypt data and manage keys

**Key Classes**:
- `AESCipher`: AES-256-CBC encryption/decryption
- `KeyDerivation`: PBKDF2 password-based key generation
- `HashUtils`: SHA-256 hashing and verification

**Key Algorithms**:
- AES-256 in CBC mode with PKCS7 padding
- PBKDF2 with SHA-256 (100,000 iterations)
- SHA-256 for integrity verification

### Core Module

**Purpose**: General utilities and file operations

**Key Classes**:
- `FileOperations`: File I/O with validation
- `CompressionHandler`: Zlib compression
- `Utils`: Helper functions (formatting, validation, UI)

## Security Considerations

### Encryption Strength
- **Algorithm**: AES-256 (military-grade)
- **Mode**: CBC with random IV
- **Key Length**: 256 bits
- **Key Derivation**: PBKDF2 with 100,000 iterations

### Steganography Strength
- **Method**: LSB encoding (reversible)
- **Capacity**: ~50% of image pixel data
- **Detection Resistance**: Depends on image selection and bit planes

### Integrity Verification
- **Hash Algorithm**: SHA-256
- **Verification**: Automatic on extract
- **Salt**: Unique 16-byte salt per operation

## Performance Characteristics

| Operation | Time (10MB) | Notes |
|-----------|-------------|-------|
| Encryption | ~100ms | AES-256-CBC |
| Decryption | ~100ms | AES-256-CBC |
| Key Derivation | ~200ms | PBKDF2, 100k iterations |
| Compression | ~50ms | Zlib level 9 |
| Decompression | ~30ms | Zlib |
| LSB Encode (4K img) | ~500ms | Depends on image size |
| LSB Decode (4K img) | ~400ms | Depends on image size |

## Scalability & Limitations

### Current Limitations
- Max file size: 500 MB (configurable)
- Max image size: Limited by available memory
- LSB capacity: ~50% of image pixel data
- Not resistant to advanced steganalysis

### Future Improvements
- Streaming encryption for large files
- Multiple encoding algorithms (DCT, DFT)
- Parallel processing
- GPU acceleration

## Security Best Practices

1. **Password Management**
   - Use 16+ character passwords
   - Mix uppercase, lowercase, digits, symbols
   - Avoid dictionary words

2. **Image Selection**
   - Use high-quality images
   - Avoid synthetic or highly compressed images
   - Use different images for different recipients

3. **File Handling**
   - Secure delete sensitive files after hiding
   - Verify extraction before sharing
   - Keep backups of important files

4. **Key Management**
   - Never hardcode passwords
   - Use environment variables or secure vaults
   - Rotate passwords periodically

## Testing Strategy

- **Unit Tests**: Individual component functionality
- **Integration Tests**: End-to-end workflows
- **Security Tests**: Hash verification, encryption validation
- **Performance Tests**: Encoding/decoding speed

## Deployment Considerations

1. **CLI Usage**: Single-machine operation
2. **Web Deployment**: Flask development/production servers
3. **Security**: Use HTTPS in production, secure file uploads
4. **Storage**: Temporary file cleanup in uploads folder
