"""
Web Interface for Autonomous Data Science Agent
Flask-based web application with file upload and visualization
"""

from flask import Flask, render_template, request, send_file, jsonify, redirect, url_for
import os
from pathlib import Path
import json
from datetime import datetime
from werkzeug.utils import secure_filename
import threading
import uuid

from main import AutonomousDataScienceAgent

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get('MAX_UPLOAD_SIZE', 50)) * 1024 * 1024
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# Create upload folder
Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)

# Store job status
jobs = {}

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def run_analysis(job_id, csv_path, target_column, output_dir):
    """Run analysis in background"""
    try:
        jobs[job_id]['status'] = 'running'
        jobs[job_id]['progress'] = 'Starting analysis...'
        
        agent = AutonomousDataScienceAgent(
            csv_path=csv_path,
            target_column=target_column,
            output_dir=output_dir
        )
        
        results = agent.run()
        
        jobs[job_id]['status'] = 'completed'
        jobs[job_id]['results'] = results
        jobs[job_id]['progress'] = 'Analysis completed!'
        
    except ValueError as e:
        # User-friendly validation errors
        jobs[job_id]['status'] = 'failed'
        error_str = str(e)
        
        # Check if it's a target detection error
        if "Cannot auto-detect a valid target column" in error_str:
            user_friendly_msg = (
                "❌ This dataset cannot be used for machine learning.\n\n"
                "The uploaded file appears to be a database or contact list with ID columns only. "
                "Machine learning requires data with predictable patterns.\n\n"
                "Please upload a dataset with:\n"
                "• A target column to predict (like 'churn', 'attrition', 'outcome')\n"
                "• Feature columns with meaningful data\n"
                "• Not all unique values (avoid ID columns, URLs, emails)\n\n"
                "Try uploading 'sample_churn_data.csv' or 'demo_employee_attrition.csv' for a working example."
            )
            jobs[job_id]['error'] = user_friendly_msg
            jobs[job_id]['progress'] = 'Dataset Validation Failed'
        else:
            jobs[job_id]['error'] = error_str
            jobs[job_id]['progress'] = f'Validation Error: {error_str}'
    except Exception as e:
        # Other errors
        jobs[job_id]['status'] = 'failed'
        error_msg = f"{type(e).__name__}: {str(e)}"
        jobs[job_id]['error'] = error_msg
        jobs[job_id]['progress'] = f'Error: {error_msg}'

@app.route('/favicon.ico')
def favicon():
    """Return empty favicon to prevent 404 errors"""
    return '', 204

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    target_column = request.form.get('target_column', '')
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        # Save file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        # Create job
        job_id = str(uuid.uuid4())
        output_dir = f"output_{job_id}"
        
        jobs[job_id] = {
            'id': job_id,
            'filename': filename,
            'status': 'pending',
            'progress': 'Uploaded successfully',
            'created_at': datetime.now().isoformat(),
            'output_dir': output_dir
        }
        
        # Start analysis in background
        thread = threading.Thread(
            target=run_analysis,
            args=(job_id, filepath, target_column if target_column else None, output_dir)
        )
        thread.start()
        
        return jsonify({
            'job_id': job_id,
            'message': 'File uploaded successfully. Analysis started.'
        })
    
    return jsonify({'error': 'Invalid file type. Only CSV files allowed.'}), 400

@app.route('/status/<job_id>')
def job_status(job_id):
    """Get job status"""
    if job_id not in jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    job = jobs[job_id]
    response = {
        'job_id': job_id,
        'status': job['status'],
        'progress': job.get('progress', ''),
        'filename': job.get('filename', '')
    }
    
    if job['status'] == 'completed':
        results = job.get('results', {})
        response['report_path'] = results.get('report_path', '')
        response['output_dir'] = job.get('output_dir', '')
        
        # Add model results
        model_results = results.get('model_results', {})
        if model_results:
            response['best_model'] = model_results.get('best_model_name', 'N/A')
            response['best_score'] = model_results.get('best_score', 0.0)
            response['is_classification'] = model_results.get('is_classification', True)
            response['metrics'] = model_results.get('metrics', {})
        
        # Get visualization files
        viz_dir = Path(job['output_dir']) / 'visualizations'
        if viz_dir.exists():
            response['visualizations'] = [f.name for f in viz_dir.glob('*.png')]
    
    elif job['status'] == 'failed':
        response['error'] = job.get('error', 'Unknown error')
    
    return jsonify(response)

@app.route('/results/<job_id>')
def results(job_id):
    """Show results page"""
    if job_id not in jobs:
        return "Job not found", 404
    
    job = jobs[job_id]
    if job['status'] != 'completed':
        return redirect(url_for('index'))
    
    return render_template('results.html', job_id=job_id, job=job)

@app.route('/download/report/<job_id>')
def download_report(job_id):
    """Download PDF report"""
    if job_id not in jobs or jobs[job_id]['status'] != 'completed':
        return "Report not found", 404
    
    report_path = jobs[job_id]['results']['report_path']
    return send_file(report_path, as_attachment=True)

@app.route('/download/viz/<job_id>/<filename>')
def download_visualization(job_id, filename):
    """Download visualization"""
    if job_id not in jobs:
        return "Job not found", 404
    
    viz_path = Path(jobs[job_id]['output_dir']) / 'visualizations' / filename
    if not viz_path.exists():
        return "File not found", 404
    
    return send_file(viz_path, as_attachment=True)

@app.route('/view/viz/<job_id>/<filename>')
def view_visualization(job_id, filename):
    """View visualization in browser"""
    if job_id not in jobs:
        return "Job not found", 404
    
    viz_path = Path(jobs[job_id]['output_dir']) / 'visualizations' / filename
    if not viz_path.exists():
        return "File not found", 404
    
    return send_file(viz_path, mimetype='image/png')

@app.route('/api/jobs')
def list_jobs():
    """List all jobs"""
    return jsonify({
        'jobs': [
            {
                'job_id': job_id,
                'filename': job['filename'],
                'status': job['status'],
                'created_at': job['created_at']
            }
            for job_id, job in jobs.items()
        ]
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Autonomous Data Science Agent - Web Interface")
    print("="*60)
    print("\nStarting web server...")
    
    # Get port from environment variable (for cloud deployment)
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    
    print(f"Open your browser and go to: http://localhost:{port}")
    print("\nPress Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    app.run(debug=debug, host='0.0.0.0', port=port)
