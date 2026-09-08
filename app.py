"""
Flask Web Application - Web dashboard for secure file sharing
Provides REST API and web interface
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from secure_sharing import SecureFileSharingSystem
from core.utils import Utils
import os
from werkzeug.utils import secure_filename
import tempfile

app = Flask(__name__)
CORS(app)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500 MB
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp'}

system = SecureFileSharingSystem()


def allowed_file(filename):
    """
    Check if file extension is allowed
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """
    Serve main page
    """
    return render_template('index.html')


@app.route('/api/hide', methods=['POST'])
def api_hide():
    """
    API endpoint for hiding file
    """
    try:
        # Validate request
        if 'cover_image' not in request.files:
            return jsonify({'error': 'No cover image provided'}), 400
        if 'secret_file' not in request.files:
            return jsonify({'error': 'No secret file provided'}), 400
        if 'password' not in request.form:
            return jsonify({'error': 'No password provided'}), 400
        
        cover_image = request.files['cover_image']
        secret_file = request.files['secret_file']
        password = request.form['password']
        compress = request.form.get('compress', 'true').lower() == 'true'
        bit_planes = int(request.form.get('bit_planes', 1))
        
        if not allowed_file(cover_image.filename):
            return jsonify({'error': 'Invalid image format'}), 400
        
        # Save uploaded files
        cover_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(cover_image.filename))
        secret_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(secret_file.filename))
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output_' + secure_filename(cover_image.filename))
        
        cover_image.save(cover_path)
        secret_file.save(secret_path)
        
        # Perform operation
        result = system.hide_file(
            cover_path, secret_path, output_path, password,
            compress=compress, bit_planes=bit_planes
        )
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'File hidden successfully',
                'output_file': os.path.basename(output_path),
                'statistics': result
            })
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/extract', methods=['POST'])
def api_extract():
    """
    API endpoint for extracting file
    """
    try:
        if 'stego_image' not in request.files:
            return jsonify({'error': 'No stego image provided'}), 400
        if 'password' not in request.form:
            return jsonify({'error': 'No password provided'}), 400
        
        stego_image = request.files['stego_image']
        password = request.form['password']
        bit_planes = int(request.form.get('bit_planes', 1))
        
        if not allowed_file(stego_image.filename):
            return jsonify({'error': 'Invalid image format'}), 400
        
        # Save uploaded file
        stego_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(stego_image.filename))
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'extracted_file')
        
        stego_image.save(stego_path)
        
        # Perform operation
        result = system.extract_file(
            stego_path, output_path, password, bit_planes=bit_planes
        )
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'File extracted successfully',
                'filename': result['filename'],
                'statistics': result
            })
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/image-info', methods=['POST'])
def api_image_info():
    """
    API endpoint for image information
    """
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        image = request.files['image']
        
        if not allowed_file(image.filename):
            return jsonify({'error': 'Invalid image format'}), 400
        
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image.filename))
        image.save(image_path)
        
        info = system.get_image_info(image_path)
        
        if 'error' not in info:
            return jsonify({'success': True, 'info': info})
        else:
            return jsonify({'success': False, 'error': info['error']}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/password-strength', methods=['POST'])
def api_password_strength():
    """
    API endpoint for password strength check
    """
    data = request.get_json()
    password = data.get('password', '')
    
    from cryptography_module import KeyDerivation
    strength = KeyDerivation.verify_key_strength(password)
    
    return jsonify(strength)


@app.route('/health')
def health():
    """
    Health check endpoint
    """
    return jsonify({'status': 'healthy'})


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
