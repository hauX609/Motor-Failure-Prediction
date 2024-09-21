import subprocess
from flask import Flask, jsonify, send_from_directory, request
import requests
import sqlite3
from datetime import datetime

app = Flask(__name__, static_folder='static', template_folder='templates')

AI_MODEL_API_URL = 'http://127.0.0.1:5001/predict'

# Fetch all motor data from SQLite database
def fetch_all_data():
    try:
        conn = sqlite3.connect('project.db')
        cursor = conn.cursor()

        query = """
            SELECT Product_Type, Rotation_Speed, Air_Temp, Torque, Load, Current, Voltage, Humidity, Timestamp
            FROM motor_data
        """

        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()

        return rows

    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

# Status endpoint to get AI model predictions and derived fields
@app.route('/status', methods=['GET'])
def status():
    try:
        data = fetch_all_data()

        results = []
        for product_type, rotation_speed, air_temp, torque, load, current, voltage, humidity, timestamp in data:
            motor_data = {
                'Temperature': [air_temp],
                'Vibration': [rotation_speed],
                'Speed': [rotation_speed],
                'Load': [load],
                'Current': [current],
                'Torque': [torque],
                'Voltage': [voltage],
                'Humidity': [humidity]
            }

            response = requests.post(AI_MODEL_API_URL, json=motor_data)
            if response.status_code == 200:
                prediction = response.json()
                energy_consumption = prediction.get('Energy Consumption', [0])[0]
                failure_event = prediction.get('Failure Event', [0])[0]
                failure_type = prediction.get('Failure Type', [['Unknown']])[0][0]
                power = prediction.get('Power', [0])[0]
                recommendation = prediction.get('Recommendation', [[0]])[0][0]
                remaining_life = prediction.get('Remaining Life', [0])[0]

                is_faulty = failure_event == 1

                results.append({
                    'Product_Type': product_type,
                    'Rotation_Speed': rotation_speed,
                    'Air_Temp': air_temp,
                    'Torque': torque,
                    'Timestamp': timestamp,
                    'Energy_Consumption': energy_consumption,
                    'Failure_Event': failure_event,
                    'Failure_Type': failure_type,
                    'Power': power,
                    'Recommendation': recommendation,
                    'Remaining_Life': remaining_life,
                    'Is_Faulty': is_faulty
                })


            else:
                results.append({
                    'Product_Type': product_type,
                    'Rotation_Speed': rotation_speed,
                    'Air_Temp': air_temp,
                    'Torque': torque,
                    'Timestamp': timestamp,
                    'Energy_Consumption': 'Error retrieving prediction',
                    'Failure_Event': 'Error retrieving prediction',
                    'Failure_Type': 'Error retrieving prediction',
                    'Power': 'Error retrieving prediction',
                    'Recommendation': 'Error retrieving prediction',
                    'Remaining_Life': 'Error retrieving prediction',
                    'Is_Faulty': False
                })

        return jsonify(results)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Refresh endpoint to manually refresh motor data by calling an update script
@app.route('/refresh', methods=['POST'])
def refresh():
    try:
        # Call the update_motor_data.py script
        subprocess.run(['python', 'update_motor_data.py'], check=True)
        return jsonify({'status': 'success', 'message': 'Data updated successfully.'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Route for serving the main index.html page
@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

# Route for serving the motor.html page
@app.route('/motor.html')
def motor():
    return send_from_directory('templates', 'motor.html')

# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)
