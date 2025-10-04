import os
import pandas as pd
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Python Analytics Server is running"}

# 🔹 Directly read a fixed CSV file from the repo
@app.get("/analyze_csv")
def analyze_csv():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "analyze_csv.csv")  # put file in repo root

    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="CSV file not found on server")

    df = pd.read_csv(csv_path)

    return {
        "average": round(float(df["Score"].mean()), 2),
        "highest": round(float(df["Score"].max()), 2),
        "lowest": round(float(df["Score"].min()), 2),
        "failure_rate": round(float((df["Score"] < 60).mean() * 100.0), 2)
    }
