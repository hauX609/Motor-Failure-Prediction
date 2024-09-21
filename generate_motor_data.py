import random
from datetime import datetime
import sqlite3

def generate_random_motor_data():
    product_types = ['M', 'L', 'H']  # Motor types
    temperatures = [random.randint(20, 80) + random.uniform(-5, 5) for _ in range(3)]  # °C with disturbance
    vibrations = [random.uniform(0.1, 1.0) + random.uniform(-0.1, 0.1) for _ in range(3)]  # mm/s with disturbance
    speeds = [random.randint(2500, 4500) + random.randint(-100, 100) for _ in range(3)]  # RPM with disturbance
    loads = [random.randint(10, 100) + random.randint(-5, 5) for _ in range(3)]  # % with disturbance
    currents = [random.uniform(0.5, 10.0) + random.uniform(-0.5, 0.5) for _ in range(3)]  # Amp with disturbance
    torques = [random.randint(20, 40) + random.randint(-2, 2) for _ in range(3)]  # Nm with disturbance
    humidities = [random.randint(30, 90) + random.randint(-5, 5) for _ in range(3)]  # % with disturbance
    timestamp = datetime.now().strftime('%d-%m-%Y %H:%M')  # Datetime

    data = []
    for i in range(3):
        data.append([
            product_types[i],
            temperatures[i],
            vibrations[i],
            speeds[i],
            loads[i],
            currents[i],
            torques[i],
            humidities[i],
            timestamp
        ])

    return data

def store_data_in_db(data, db_path='project.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS motor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_type TEXT,
            temperature REAL,
            vibration REAL,
            speed INTEGER,
            load INTEGER,
            current REAL,
            torque INTEGER,
            humidity INTEGER,
            timestamp TEXT
        )
    ''')

    # Clear previous data
    cursor.execute('DELETE FROM motor_data')

    # Reset the auto-increment counter
    cursor.execute('DELETE FROM sqlite_sequence WHERE name="motor_data"')

    # Insert new data into the table
    cursor.executemany('''
        INSERT INTO motor_data (
            product_type, temperature, vibration, speed, load, current, torque, humidity, timestamp
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', data)

    conn.commit()
    conn.close()

def main():
    data = generate_random_motor_data()
    store_data_in_db(data)

if __name__ == '__main__':
    main()