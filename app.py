from fastapi import FastAPI, Query
import pandas as pd
import os

app = FastAPI()

# Directory where Blazor saves uploaded files
UPLOAD_DIR = "wwwroot/uploads"

@app.get("/")
def root():
    return {"message": "Python Analytics Server is running"}

@app.get("/analyze_csv")
def analyze_csv(filename: str = Query(...)):
    filepath = os.path.join(UPLOAD_DIR, filename)

    if not os.path.exists(filepath):
        return {"error": f"File not found: {filepath}"}

    try:
        df = pd.read_csv("test.csv")
    except Exception as e:
        return {"error": f"Failed to read CSV: {str(e)}"}

    result = {
        "rows": len(df),
        "columns": list(df.columns),
        "average": df['Score'].mean() if 'Score' in df else None,
        "highest": df['Score'].max() if 'Score' in df else None,
        "lowest": df['Score'].min() if 'Score' in df else None,
        "fail_rate": float((df['Score'] < 66).mean()) if 'Score' in df else None
    }

    return result
