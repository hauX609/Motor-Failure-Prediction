import numpy as np
import pandas as pd

# Initialize an empty list to store the generated data
data = []

# Define motor types and their characteristics
motor_types = {
    'M': {'temp_range': (20, 80), 'vib_range': (0, 5), 'speed_range': (1000, 2000), 'load_range': (0, 50), 'current_range': (0, 25), 'torque_range': (0, 250)},
    'L': {'temp_range': (30, 90), 'vib_range': (1, 7), 'speed_range': (1500, 2500), 'load_range': (20, 70), 'current_range': (10, 35), 'torque_range': (100, 350)},
    'H': {'temp_range': (40, 100), 'vib_range': (2, 10), 'speed_range': (2000, 3000), 'load_range': (50, 100), 'current_range': (20, 50), 'torque_range': (200, 500)}
}

# Define failure types and their numerical values
failure_types = {
    'No Failure': 0,
    'Bearing Failure': 1,
    'Overheating': 2,
    'Vibration Issue': 3,
    'Electrical Failure': 4,
    'Unknown Failure': 5
}

# Define recommendations for different failure types
recommendations = {
    'No Failure': 'N/A',
    'Bearing Failure': 'Replace bearings',
    'Overheating': 'Check cooling system',
    'Vibration Issue': 'Balance the motor',
    'Electrical Failure': 'Inspect electrical connections',
    'Unknown Failure': 'Perform full inspection'
}

# Define probabilities for each failure type
failure_probabilities = {
    'No Failure': 0.2,
    'Bearing Failure': 0.16,
    'Overheating': 0.16,
    'Vibration Issue': 0.16,
    'Electrical Failure': 0.16,
    'Unknown Failure': 0.16
}

# Generate data
for _ in range(5000):  # Adjust the number of samples as needed
    motor_type = np.random.choice(['M', 'L', 'H'])
    characteristics = motor_types[motor_type]
    
    temperature = np.random.uniform(*characteristics['temp_range'])
    vibration = np.random.uniform(*characteristics['vib_range'])
    speed = np.random.uniform(*characteristics['speed_range'])
    load = np.random.uniform(*characteristics['load_range'])
    current = np.random.uniform(*characteristics['current_range'])
    torque = np.random.uniform(*characteristics['torque_range'])
    
    # Determine failure type based on weighted random choice
    failure_type = np.random.choice(
        list(failure_types.values()), 
        p=[failure_probabilities[key] for key in failure_types]
    )
    
    # Calculate additional features
    humidity = np.random.uniform(0, 100)
    power = speed * torque / 9550  # Simplified power calculation
    energy_consumption = power * np.random.uniform(0.5, 1.5)  # Introduce some variability
    remaining_life = np.random.uniform(100, 500) if failure_type != failure_types['No Failure'] else np.random.uniform(500, 1000)
    recommendation = recommendations.get(failure_type, 'Unknown Recommendation')
    
    # Append the generated data to the list
    data.append({
        'motor_type': motor_type,
        'temperature': temperature,
        'vibration': vibration,
        'speed': speed,
        'load': load,
        'current': current,
        'torque': torque,
        'failure_type': failure_type,
        'humidity': humidity,
        'energy_consumption': energy_consumption,
        'remaining_life': remaining_life,
        'recommendation': recommendation
    })

# Convert the list to a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv('motor_data1.csv', index=False)