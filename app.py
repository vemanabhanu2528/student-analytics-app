from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import numpy as np
from datetime import datetime
import os
from analytics import StudentAnalytics
from ml_predictor import PerformancePredictor
from report_generator import ReportGenerator

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize components
analytics = StudentAnalytics()
predictor = PerformancePredictor()
report_gen = ReportGenerator()

# Sample data for demo
SAMPLE_DATA = None

def get_sample_data():
    """Generate sample student data for demonstration"""
    np.random.seed(42)
    n_students = 100
    
    data = {
        'student_id': [f'STU{str(i).zfill(4)}' for i in range(1, n_students + 1)],
        'name': [f'Student {i}' for i in range(1, n_students + 1)],
        'math': np.random.randint(40, 100, n_students),
        'science': np.random.randint(35, 100, n_students),
        'english': np.random.randint(45, 100, n_students),
        'history': np.random.randint(40, 95, n_students),
        'attendance': np.random.randint(60, 100, n_students),
        'assignments_submitted': np.random.randint(5, 20, n_students),
        'total_assignments': [20] * n_students,
        'study_hours': np.random.randint(5, 30, n_students)
    }
    
    df = pd.DataFrame(data)
    df['average_grade'] = df[['math', 'science', 'english', 'history']].mean(axis=1).round(2)
    return df

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_data():
    """Upload student data CSV/Excel file"""
    global SAMPLE_DATA
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        # Save file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # Read file based on extension
        if file.filename.endswith('.csv'):
            SAMPLE_DATA = pd.read_csv(filepath)
        elif file.filename.endswith(('.xlsx', '.xls')):
            SAMPLE_DATA = pd.read_excel(filepath)
        else:
            return jsonify({'error': 'Unsupported file format. Use CSV or Excel'}), 400
        
        return jsonify({
            'message': 'File uploaded successfully',
            'rows': len(SAMPLE_DATA),
            'columns': list(SAMPLE_DATA.columns)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/data/summary')
def get_summary():
    """Get summary statistics of student data"""
    global SAMPLE_DATA
    
    if SAMPLE_DATA is None:
        SAMPLE_DATA = get_sample_data()
    
    summary = analytics.get_summary_stats(SAMPLE_DATA)
    return jsonify(summary)

@app.route('/api/data/visualizations')
def get_visualizations():
    """Get data for various visualizations"""
    global SAMPLE_DATA
    
    if SAMPLE_DATA is None:
        SAMPLE_DATA = get_sample_data()
    
    viz_data = analytics.get_visualization_data(SAMPLE_DATA)
    return jsonify(viz_data)

@app.route('/api/predictions', methods=['POST'])
def predict_performance():
    """Predict student performance using ML"""
    global SAMPLE_DATA
    
    if SAMPLE_DATA is None:
        SAMPLE_DATA = get_sample_data()
    
    try:
        # Train model if not already trained
        if not predictor.is_trained:
            predictor.train(SAMPLE_DATA)
        
        # Get predictions
        predictions = predictor.predict_all(SAMPLE_DATA)
        
        return jsonify({
            'predictions': predictions,
            'model_accuracy': predictor.get_accuracy()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/student/<student_id>')
def get_student_details(student_id):
    """Get detailed analytics for a specific student"""
    global SAMPLE_DATA
    
    if SAMPLE_DATA is None:
        SAMPLE_DATA = get_sample_data()
    
    student_data = analytics.get_student_profile(SAMPLE_DATA, student_id)
    if student_data is None:
        return jsonify({'error': 'Student not found'}), 404
    
    return jsonify(student_data)

@app.route('/api/export/excel', methods=['POST'])
def export_excel():
    """Export analytics report to Excel"""
    global SAMPLE_DATA
    
    if SAMPLE_DATA is None:
        SAMPLE_DATA = get_sample_data()
    
    try:
        filepath = report_gen.generate_excel_report(SAMPLE_DATA)
        return send_file(filepath, as_attachment=True, download_name='student_analytics_report.xlsx')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export/pdf', methods=['POST'])
def export_pdf():
    """Export analytics report to PDF"""
    global SAMPLE_DATA
    
    if SAMPLE_DATA is None:
        SAMPLE_DATA = get_sample_data()
    
    try:
        filepath = report_gen.generate_pdf_report(SAMPLE_DATA)
        return send_file(filepath, as_attachment=True, download_name='student_analytics_report.pdf')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/data/reset', methods=['POST'])
def reset_data():
    """Reset to sample data"""
    global SAMPLE_DATA
    SAMPLE_DATA = get_sample_data()
    predictor.reset()
    return jsonify({'message': 'Data reset to sample dataset'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
