
# Motor Failure Prediction API

This project provides an API for predicting motor failure types, providing recommendations, estimating remaining life, and calculating energy consumption and power.

## Project Structure

```
motor_failure_prediction/
├── data/
│   └── motor_data.csv
├── models/
│   └── model.pkl
├── notebooks/
│   ├── data_preprocessing.ipynb
│   └── model_training.ipynb
├── src/
│   ├── __init__.py
│   ├── data_preprocessing.py
│   ├── model_training.py
│   ├── prediction_service.py
│   └── utils.py
├── app.py
├── requirements.txt
└── README.md
```

## API Endpoints

### Root Endpoint
- **URL**: `/`
- **Method**: GET
- **Description**: Returns a welcome message.

### Predict Endpoint
- **URL**: `/predict`
- **Method**: POST
- **Description**: Handles different actions (`predict`, `recommendations`, `energy`) based on the request body.
- **Request Body**:
  - For prediction:
    ```json
    {
        "action": "predict",
        "motor_data": {
            "motor_type": 1,
            "speed": 1200,
            "temperature": 32,
            "humidity": 52,
            "load": 12,
            "current": 5.5,
            "torque": 22,
            "vibration": 0.15
        }
    }
    ```
  - For recommendations:
    ```json
    {
        "action": "recommendations",
        "motor_data": {
            "motor_type": 1,
            "speed": 1200,
            "temperature": 32,
            "humidity": 52,
            "load": 12,
            "current": 5.5,
            "torque": 22,
            "vibration": 0.15
        }
    }
    ```
  - For energy calculation:
    ```json
    {
        "action": "energy",
        "energy_data": {
            "current": 5.5,
            "voltage": 220,
            "time": 2
        }
    }
    ```

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd motor_failure_prediction
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the FastAPI application:
   ```bash
   python3 app.py
   ```

## Model Metrics

- **Accuracy**: 1.0
- **Precision**: 1.0
- **F1 Score**: 1.0

## Feature Importance

| Feature      | Importance |
|--------------|-------------|
| temperature  | 0.200000    |
| motor_type   | 0.142857    |
| speed        | 0.128571    |
| humidity     | 0.128571    |
| load         | 0.128571    |
| current      | 0.128571    |
| vibration    | 0.100000    |
| torque       | 0.042857    |

## License

This project is licensed under the MIT License.
