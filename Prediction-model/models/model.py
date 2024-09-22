import sys
import os

# Add the root directory of the project to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Train and save the model
from src.data_preprocessing import load_data, preprocess_data, split_data
from src.model_training import train_model, evaluate_model, save_model
import os

# Load and preprocess data
data_path = '/Users/harshitgupta/Downloads/Projects/MotorFailure-Prediction/Prediction-model/data/motor_data.csv'
data = load_data(data_path)
data = preprocess_data(data)

# Split data
target_column = 'failure_type'
X_train, X_test, y_train, y_test = split_data(data, target_column)

# Train the model
model = train_model(X_train, y_train)

# Evaluate the model
report = evaluate_model(model, X_test, y_test)
print(report)

# Save the model
model_path = 'Motor-Failure-Prediction/models/model.pkl'
os.makedirs('Motor-Failure-Prediction/models', exist_ok=True)
save_model(model, model_path)