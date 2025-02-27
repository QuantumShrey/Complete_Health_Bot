from flask import Flask, request, jsonify, render_template
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import json
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

# Print current directory and contents to debug
print("Current directory:", os.getcwd())
print("Contents of current directory:", os.listdir())
print("Contents of data directory:", os.listdir('data'))

# Load and prepare the data
training_dataset = pd.read_csv('data/Training.csv')
test_dataset = pd.read_csv('data/Testing.csv')

X = training_dataset.iloc[:, 0:132].values
y = training_dataset.iloc[:, -1].values

# Dimensionality Reduction
dimensionality_reduction = training_dataset.groupby(training_dataset['prognosis']).max()

# Encode labels
labelencoder = LabelEncoder()
y = labelencoder.fit_transform(y)

# Train the model
classifier = DecisionTreeClassifier()
classifier.fit(X, y)

# Save column information
cols = training_dataset.columns[:-1]

# Load doctors dataset
doc_dataset = pd.read_csv('data/doctors_dataset.csv', names=['Name', 'Description'])
diseases = dimensionality_reduction.index
diseases = pd.DataFrame(diseases)

doctors = pd.DataFrame()
doctors['name'] = doc_dataset['Name']
doctors['link'] = doc_dataset['Description']
doctors['disease'] = diseases['prognosis']

# Add these lines after creating the Flask app
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/get_symptoms', methods=['GET'])
def get_symptoms():
    print("Get symptoms endpoint called")
    symptoms_list = cols.tolist()
    print(f"Returning {len(symptoms_list)} symptoms")
    return jsonify({'symptoms': symptoms_list})

@app.route('/predict', methods=['POST'])
def predict():
    print("Predict endpoint called")
    try:
        # Get symptoms from request
        symptoms = request.json.get('symptoms', [])
        print(f"Received symptoms: {symptoms}")
        
        if not symptoms:
            return jsonify({'error': 'No symptoms provided'}), 400

        # Create input array
        input_data = np.zeros(len(cols))
        for symptom in symptoms:
            if symptom in cols:
                input_data[cols.get_loc(symptom)] = 1

        # Make prediction
        prediction = classifier.predict([input_data])
        disease = labelencoder.inverse_transform(prediction)[0]

        # Get relevant doctor information
        doctor_info = doctors[doctors['disease'] == disease]
        if len(doctor_info) > 0:
            doctor_info = doctor_info.iloc[0]
            doctor_name = doctor_info['name']
            doctor_link = doctor_info['link']
        else:
            doctor_name = "General Practitioner"
            doctor_link = "#"

        # Calculate confidence using numpy's where function
        disease_symptoms = dimensionality_reduction.loc[disease].values
        disease_symptoms = np.where(disease_symptoms >= 1)[0]
        matching_symptoms = [s for s in symptoms if s in cols[disease_symptoms].tolist()]
        
        if len(disease_symptoms) > 0:
            confidence_level = (len(matching_symptoms) / len(disease_symptoms)) * 100
        else:
            confidence_level = 0

        response = {
            'disease': disease,
            'confidence': round(confidence_level, 2),
            'doctor_name': doctor_name,
            'doctor_link': doctor_link,
            'symptoms_present': symptoms,
            'symptoms_given': cols[disease_symptoms].tolist()
        }

        print(f"Sending response: {response}")
        return jsonify(response)

    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        import traceback
        traceback.print_exc()  # This will print the full error traceback
        return jsonify({'error': str(e)}), 500

@app.route('/test-static')
def test_static():
    return """
    <html>
        <head>
            <link rel="stylesheet" href="/static/styles.css">
        </head>
        <body>
            <h1>Testing Static Files</h1>
            <script src="/static/script.js"></script>
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True, port=5000)