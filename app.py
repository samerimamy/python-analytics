from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
from io import StringIO

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Python Analytics Server is running"}

# 🔹 must be POST, not GET
@app.post("/analyze_csv")
async def analyze_csv(file: UploadFile = File(...), pass_mark: float = 60.0):
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
