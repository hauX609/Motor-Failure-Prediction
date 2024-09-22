import joblib
import pandas as pd

def load_model(file_path):
    model = joblib.load(file_path)
    return model

def predict_failure(model, data):
    prediction = model.predict(data)
    return prediction

def calculate_energy_consumption(current, voltage, time):
    power = current * voltage
    energy_consumption = power * time
    return energy_consumption, power

def provide_recommendations(failure_type):
    recommendations = {
        0: "Check motor bearings and lubrication.",
        1: "Inspect and replace worn-out parts.",
        2: "Ensure proper cooling and ventilation.",
        3: "Check electrical connections and insulation.",
        4: "Perform regular maintenance and inspections."
    }
    return recommendations.get(failure_type, "No recommendation available.")