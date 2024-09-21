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
        .catch(error => {
            console.error('Error fetching motor data:', error);
            alert('Failed to fetch motor data. Please try again later.');
        });
}

// Function to display motor data in a table
function displayMotorData(data) {
    const motorTable = document.getElementById('motorTable');
    if (!motorTable) {
        console.error('Motor table not found');
        return;
    }

    // Create table header
    motorTable.innerHTML = `
        <thead>
            <tr>
                <th>Image</th>
                <th>Product Type</th>
                <th>Rotation Speed</th>
                <th>Air Temp</th>
                <th>Torque</th>
                <th>Timestamp</th>
                <th>Status</th>
                <th>Predicted Failure Type</th>
                <th>Predicted Recommended Action</th>
            </tr>
        </thead>
        <tbody>
        </tbody>
    `;

    const tbody = motorTable.querySelector('tbody');

    data.forEach(motor => {
        const row = document.createElement('tr');

        // Determine the status color based on failure prediction
        const statusClass = motor.Is_Faulty ? 'red' : 'green';

        row.innerHTML = `
            <td><img src="static/images/motor.png" alt="${motor.Product_Type} Motor"></td>
            <td>${motor.Product_Type}</td>
            <td>${motor.Rotation_Speed}</td>
            <td>${motor.Air_Temp}</td>
            <td>${motor.Torque}</td>
            <td>${motor.Timestamp}</td>
            <td><div class="status-light ${statusClass}"></div></td>
            <td>${motor.Predicted_Failure_Type}</td>
            <td>${motor.Predicted_Recommended_Action}</td>
        `;

        tbody.appendChild(row);
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
        .catch(error => {
            console.error('Error fetching alerts:', error);
            alert('Failed to fetch alerts. Please try again later.');
        });
}

// Function to display alerts in the alerts container
function displayAlerts(alerts) {
    const alertsContainer = document.getElementById('alertsContainer');
    if (!alertsContainer) {
        console.error('Alerts container not found');
        return;
    }

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

// Function to refresh motor data
function refreshData() {
    fetch('/refresh', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            console.log('Data updated successfully.');
            fetchMotorData(); // Reload the motor data to reflect the updated data
        } else {
            console.error('Error updating data:', data.message);
            alert('Failed to update data. Please try again later.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to update data. Please try again later.');
    });
}

// Function to toggle between showing all motors and faulty motors only
function toggleFaultyMotors() {
    const button = document.getElementById('toggleButton');
    const motorTable = document.getElementById('motorTable');

    if (!button || !motorTable) {
        console.error('Toggle button or motor table not found');
        return;
    }

    const showingFaultyOnly = button.innerText === 'Show Faulty Motors Only';

    Array.from(motorTable.querySelectorAll('tbody tr')).forEach(row => {
        const statusCell = row.cells[6];
        const statusClass = statusCell.querySelector('.status-light').classList.contains('red');
        if (showingFaultyOnly && !statusClass) {
            row.style.display = 'none';
        } else {
            row.style.display = '';
        }
    });

    button.innerText = showingFaultyOnly ? 'Show All Motors' : 'Show Faulty Motors Only';
}
