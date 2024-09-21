import sqlite3
import random
from datetime import datetime

def generate_random_motor_data():
    product_types = ['M', 'L', 'H']
    rotation_speeds = [random.randint(2500, 4500) for _ in range(3)]
    air_temps = [random.randint(20, 80) for _ in range(3)]
    torques = [random.randint(20, 40) for _ in range(3)]
    timestamp = datetime.now().strftime('%d-%m-%Y %H:%M')

    data = []
    for i in range(3):
        data.append((product_types[i], rotation_speeds[i], air_temps[i], torques[i], timestamp))

    return data

def update_database():
    data = generate_random_motor_data()

    try:
        conn = sqlite3.connect('Project.db')
        cursor = conn.cursor()

        # Clear the existing data in the table
        cursor.execute("DELETE FROM motor_data")

        # Insert the new random data
        cursor.executemany("INSERT INTO motor_data (Product_Type, Rotation_Speed, Air_Temp, Torque, Timestamp) VALUES (?, ?, ?, ?, ?)", data)

        conn.commit()
        conn.close()

        print('Database updated successfully.')

    except Exception as e:
        print(f'Error updating database: {e}')

if __name__ == "__main__":
    update_database()
