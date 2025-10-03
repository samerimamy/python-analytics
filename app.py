from fastapi import UploadFile, File, HTTPException
from io import StringIO

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
