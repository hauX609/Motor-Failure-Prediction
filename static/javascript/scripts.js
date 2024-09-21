document.addEventListener('DOMContentLoaded', () => {
    fetchMotorData();
    fetchAlerts();
});

// Function to fetch motor data and display it
function fetchMotorData() {
    fetch('http://127.0.0.1:5000/status')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Motor data fetched:', data);
            displayMotorData(data);
        })
        .catch(error => console.error('Error fetching motor data:', error));
}

// Function to display motor data in the motor grid
function displayMotorData(data) {
    const motorGrid = document.getElementById('motorGrid');
    motorGrid.innerHTML = ''; // Clear any existing content

    data.forEach(motor => {
        const motorBox = document.createElement('div');
        motorBox.className = 'motor-box';
        motorBox.innerHTML = `
            <p>Product Type: ${motor.Product_Type}</p>
            <p>Rotation Speed: ${motor.Rotation_Speed}</p>
            <p>Air Temp: ${motor.Air_Temp}</p>
            <p>Torque: ${motor.Torque}</p>
            <p>Timestamp: ${motor.Timestamp}</p>
            <p>Predicted Failure Type: ${motor.Predicted_Failure_Type}</p>
            <p>Predicted Recommended Action: ${motor.Predicted_Recommended_Action}</p>
        `;
        motorGrid.appendChild(motorBox);
    });
}

// Function to fetch and display alerts
function fetchAlerts() {
    fetch('http://127.0.0.1:5000/alerts')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(alerts => {
            console.log('Alerts fetched:', alerts);
            displayAlerts(alerts);
        })
        .catch(error => console.error('Error fetching alerts:', error));
}

// Function to display alerts in the alerts container
function displayAlerts(alerts) {
    const alertsContainer = document.getElementById('alertsContainer');
    alertsContainer.innerHTML = ''; // Clear any existing content

    alerts.forEach(alert => {
        const alertBox = document.createElement('div');
        alertBox.className = 'alert-box';
        alertBox.innerHTML = `
            <p>Product Type: ${alert.Product_Type}</p>
            <p>Status: ${alert.status}</p>
        `;
        alertsContainer.appendChild(alertBox);
    });
}

// Function to toggle between showing all motors and faulty motors only
function toggleFaultyMotors() {
    const button = document.getElementById('toggleButton');
    const motorGrid = document.getElementById('motorGrid');

    if (button.innerText === 'Show Faulty Motors Only') {
        const faultyMotors = Array.from(motorGrid.children).filter(motorBox => {
            return motorBox.querySelector('p:nth-child(6)').innerText.includes('failure');
        });
        motorGrid.innerHTML = '';
        faultyMotors.forEach(motorBox => motorGrid.appendChild(motorBox));
        button.innerText = 'Show All Motors';
    } else {
        fetchMotorData(); // Refresh motor data to show all motors
        button.innerText = 'Show Faulty Motors Only';
    }
}
