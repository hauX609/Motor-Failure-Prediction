import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from src.prediction_service import load_model, predict_failure, calculate_energy_consumption, provide_recommendations

app = FastAPI()

class MotorData(BaseModel):
    motor_type: int
    speed: float
    temperature: float
    humidity: float
    load: float
    current: float
    torque: float
    vibration: float

class EnergyData(BaseModel):
    current: float
    voltage: float
    time: float

class RequestData(BaseModel):
    action: str
    motor_data: MotorData = None
    energy_data: EnergyData = None

model = load_model("/Users/harshitgupta/Downloads/Projects/MotorFailure-Prediction/Prediction-model/models/model.pkl")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Motor Failure Prediction API"}

@app.post("/predict")
def predict(data: RequestData):
    if data.action == "predict":
        if data.motor_data is None:
            raise HTTPException(status_code=400, detail="Motor data is required for prediction")
        data_dict = data.motor_data.dict()
        df = pd.DataFrame([data_dict])
        prediction = predict_failure(model, df)
        return {"failure_type": int(prediction[0])}
    
    elif data.action == "recommendations":
        if data.motor_data is None:
            raise HTTPException(status_code=400, detail="Motor data is required for recommendations")
        data_dict = data.motor_data.dict()
        df = pd.DataFrame([data_dict])
        prediction = predict_failure(model, df)
        recommendations = provide_recommendations(int(prediction[0]))
        return {"recommendations": recommendations}
    
    elif data.action == "energy":
        if data.energy_data is None:
            raise HTTPException(status_code=400, detail="Energy data is required for energy calculation")
        energy_data = data.energy_data
        energy_consumption, power = calculate_energy_consumption(energy_data.current, energy_data.voltage, energy_data.time)
        return {"energy_consumption": energy_consumption, "power": power}
    
    else:
        raise HTTPException(status_code=400, detail="Invalid action")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,port=5001)