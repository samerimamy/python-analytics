import os
import pandas as pd
from fastapi import FastAPI, UploadFile, File, HTTPException
from io import StringIO

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Python Analytics Server is running"}

@app.get("/mis")
def mis_analytics():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "students_mis.csv")

    df = pd.read_csv(csv_path)

    result = {
        "Total": int(len(df)),
        "BySemester": df["Semester"].value_counts().to_dict(),
        "ByCourse": df["Course"].value_counts().to_dict(),
        "EmploymentRate": float(df["EmployedWithin6Months"].mean()),
        "AverageGPA": float(df["GPA"].mean())
    }
    return result

# 🔹 New endpoint for uploads
@app.post("/analyze_csv")
async def analyze_csv(file: UploadFile = File(...), pass_mark: float = 60.0):
    try:
        content = (await file.read()).decode("utf-8", errors="ignore")
        df = pd.read_csv(StringIO(content))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad CSV: {e}")

    if "Score" not in df.columns:
        raise HTTPException(status_code=400, detail="CSV must contain a 'Score' column")

    avg = float(df["Score"].mean())
    hi = float(df["Score"].max())
    lo = float(df["Score"].min())
    fail_rate = float((df["Score"] < pass_mark).mean() * 100.0)

    return {
        "average": round(avg, 2),
        "highest": round(hi, 2),
        "lowest": round(lo, 2),
        "failure_rate": round(fail_rate, 2)
    }
