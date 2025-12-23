from fastapi import FastAPI
import joblib
import numpy as np

app = FastAPI()
model = joblib.load("model/model.joblib")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(value: float):
    prediction = model.predict(np.array([[value, value, value, value]]))
    return {"prediction": int(prediction[0])}
