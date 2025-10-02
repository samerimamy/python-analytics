from fastapi import FastAPI, UploadFile, File
import pandas as pd
import os

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Python Analytics Server is running"}

# --- Old MIS endpoint ---
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

# --- New SPI endpoint ---
@app.post("/analyze_csv/")
async def analyze_csv(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)

    avg_score = df['Score'].mean()
    max_score = df['Score'].max()
    min_score = df['Score'].min()
    fail_rate = (df['Score'] < 50).mean() * 100

    return {
        "average": round(avg_score, 2),
        "highest": int(max_score),
        "lowest": int(min_score),
        "failure_rate": round(fail_rate, 2)
    }
