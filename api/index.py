"""
Lightweight API for Vercel deployment
This is a minimal Flask app that provides basic endpoints
Heavy ML processing should be done elsewhere or optimized
"""

from flask import Flask, jsonify, request
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'message': 'Autonomous Data Science Agent API',
        'status': 'online',
        'note': 'Full ML processing requires local deployment or cloud compute instance'
    })

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy'})

@app.route('/api/info')
def info():
    return jsonify({
        'name': 'Autonomous Data Science Agent',
        'version': '1.0.0',
        'features': [
            'CSV Data Loading',
            'Automatic Data Cleaning',
            'Feature Engineering',
            'AutoML Model Selection',
            'Visualization Generation',
            'PDF Report Creation'
        ],
        'deployment': 'vercel-serverless',
        'note': 'For full functionality, please run locally or use a dedicated compute instance'
    })

# Vercel serverless function handler
def handler(request):
    with app.request_context(request.environ):
        return app.full_dispatch_request()
