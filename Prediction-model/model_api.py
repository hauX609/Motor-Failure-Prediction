from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Load the trained models
failure_model = joblib.load('failure_model.pkl')
life_model = joblib.load('life_model.pkl')

# Initialize the Flask application
app = Flask(__name__)

# Define a mapping for failure types
failure_type_mapping = {
    0: 'No Failure',
    1: 'Bearing Failure',
    2: 'Overheating',
    3: 'Vibration Issue',
    4: 'Electrical Failure',
    5: 'Unknown Failure'
}

# Define a route for the default URL, which loads the home page
@app.route('/')
def home():
    return "Motor Failure Prediction API"

# Define a route for making predictions
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        
        # Extract features from the request data
        features = np.array(data['features']).reshape(1, -1)
        
        # Ensure the number of features matches the expected number
        expected_num_features = 8  # Update this based on your actual number of features
        if features.shape[1] != expected_num_features:
            return jsonify({"error": f"Incorrect number of features. Expected {expected_num_features}, got {features.shape[1]}"}), 400
        
        # Create a DataFrame for the features
        feature_names = ['motor_type', 'temperature', 'vibration', 'speed', 'torque', 'load','current','humidity']
        df = pd.DataFrame(features, columns=feature_names)
        
        # Recreate the label encoder and scaler
        label_encoder = LabelEncoder()
        label_encoder.fit(['L', 'M', 'H'])  # Assuming these are the categories in 'motor_type'
        df['motor_type'] = label_encoder.transform(df['motor_type'])
        
        # Derive power and energy consumption
        df['power'] = df['speed'].astype(float) * df['torque'].astype(float) / 9550
        df['energy_consumption'] = df['power'] * df['load'].astype(float) / 100
        
        # Normalize/scale the data
        scaler = StandardScaler()
        scaler.fit(df)  # Fit the scaler on the input data
        scaled_features = scaler.transform(df)
        
        # Make predictions using the loaded models
        failure_prediction = failure_model.predict(scaled_features)[0]
        life_prediction = life_model.predict(scaled_features)[0]
        
        # Map failure types to recommendations
        recommendations = {
            0: 'N/A',
            1: 'Replace bearings',
            2: 'Check cooling system',
            3: 'Balance the motor',
            4: 'Inspect electrical connections',
            5: 'Perform full inspection'
        }
        
        recommendation = recommendations.get(failure_prediction, 'Unknown Recommendation')
        
        failure_prediction_name = failure_type_mapping.get(failure_prediction, 'Unknown Failure Type')
        
        # Return the predictions as a JSON response
        response = {
            'predicted_failure_type': failure_prediction_name,
            'predicted_remaining_life': float(life_prediction),
            'recommendation': recommendation
        }
        
        return jsonify(response)
    
    except Exception as e:
        # Log the error and return a 500 response
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# Run the Flask application on port 5001
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)