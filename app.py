import os
import sys
from flask import Flask, render_template, request, jsonify, redirect, url_for
import subprocess
import threading
import logging

app = Flask(__name__)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


process_status = {
    'running': False,
    'output': '',
    'error': ''
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/train')
def train_page():
    return render_template('train.html')

@app.route('/inference')
def inference_page():
    return render_template('inference.html')

@app.route('/run_collect_images')
def run_collect_images():
    try:
        
        process = subprocess.Popen([
            sys.executable, 
            os.path.join(os.path.dirname(__file__), 'collect_imgs.py')
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        stdout, stderr = process.communicate()
        
        return jsonify({
            'success': process.returncode == 0,
            'stdout': stdout,
            'stderr': stderr,
            'returncode': process.returncode
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/run_create_dataset')
def run_create_dataset():
    try:
      
        process = subprocess.Popen([
            sys.executable, 
            os.path.join(os.path.dirname(__file__), 'create_dataset.py')
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        stdout, stderr = process.communicate()
        
        return jsonify({
            'success': process.returncode == 0,
            'stdout': stdout,
            'stderr': stderr,
            'returncode': process.returncode
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/run_train_classifier')
def run_train_classifier():
    try:
       
        process = subprocess.Popen([
            sys.executable, 
            os.path.join(os.path.dirname(__file__), 'train_classifier.py')
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        stdout, stderr = process.communicate()
        
        return jsonify({
            'success': process.returncode == 0,
            'stdout': stdout,
            'stderr': stderr,
            'returncode': process.returncode
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/run_inference')
def run_inference():
    try:
        
        model_path = os.path.join(os.path.dirname(__file__), 'model.p')
        if not os.path.exists(model_path):
            return jsonify({
                'success': False,
                'error': 'Model file not found. Please train the model first.'
            })
        
        process = subprocess.Popen([
            sys.executable, 
            os.path.join(os.path.dirname(__file__), 'inference_classifier.py')
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        stdout, stderr = process.communicate()
        
        return jsonify({
            'success': process.returncode == 0,
            'stdout': stdout,
            'stderr': stderr,
            'returncode': process.returncode
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':

    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
    
    app.run(debug=True, host='0.0.0.0', port=5001)