"""
File upload endpoint for Vercel
Stores files and queues them for processing
"""

from flask import Flask, request, jsonify
import os
import json
from datetime import datetime
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload', methods=['POST'])
def upload():
    """Handle file upload"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        job_id = str(uuid.uuid4())
        
        # In production, you would:
        # 1. Upload to cloud storage (S3, GCS, etc.)
        # 2. Queue processing job (SQS, Cloud Tasks, etc.)
        # 3. Return job ID for status tracking
        
        return jsonify({
            'job_id': job_id,
            'message': 'File uploaded successfully',
            'note': 'Processing requires external compute. Please run locally for full functionality.',
            'filename': filename,
            'timestamp': datetime.now().isoformat()
        })
    
    return jsonify({'error': 'Invalid file type. Only CSV files allowed.'}), 400

# Vercel handler
def handler(request):
    with app.request_context(request.environ):
        return app.full_dispatch_request()
