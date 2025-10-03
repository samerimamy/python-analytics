from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
from io import StringIO
import os

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Python Analytics Server is running"}

# ✅ Existing GET endpoint (fixed file on server)
@app.get("/analyze_csv")
def analyze_csv_get():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "analyze_csv.csv")

    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="CSV file not found on server")

    df = pd.read_csv(csv_path)
    return {
        "average": round(float(df["Score"].mean()), 2),
        "highest": round(float(df["Score"].max()), 2),
        "lowest": round(float(df["Score"].min()), 2),
        "failure_rate": round(float((df["Score"] < 60).mean() * 100.0), 2)
    }

# 🔹 New POST endpoint for Blazor uploads
@app.post("/analyze_csv")
async def analyze_csv_post(file: UploadFile = File(...), pass_mark: float = 60.0):
    try:
        content = (await file.read()).decode("utf-8", errors="ignore")
        df = pd.read_csv(StringIO(content))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad CSV: {e}")

    if "Score" not in df.columns:
        raise HTTPException(status_code=400, detail="CSV must contain a 'Score' column")

    return {
        "average": round(float(df["Score"].mean()), 2),
        "highest": round(float(df["Score"].max()), 2),
        "lowest": round(float(df["Score"].min()), 2),
        "failure_rate": round(float((df["Score"] < pass_mark).mean() * 100.0), 2)
    }
