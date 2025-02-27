import os
import sys

def check_setup():
    errors = []
    
    # Check directories
    required_dirs = ['static', 'templates', 'data']
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            errors.append(f"Missing directory: {dir_name}")
    
    # Check files
    required_files = [
        'app.py',
        'static/styles.css',
        'static/script.js',
        'templates/index.html',
        'templates/services.html',
        'data/Training.csv',
        'data/Testing.csv',
        'data/doctors_dataset.csv'
    ]
    
    for file_name in required_files:
        if not os.path.exists(file_name):
            errors.append(f"Missing file: {file_name}")
    
    # Check Python packages
    try:
        import flask
        import pandas
        import numpy
        import sklearn
    except ImportError as e:
        errors.append(f"Missing package: {str(e)}")
    
    if errors:
        print("❌ Setup check failed!")
        for error in errors:
            print(f"  - {error}")
    else:
        print("✅ Setup check passed! All required files and packages are present.")

if __name__ == "__main__":
    check_setup() 