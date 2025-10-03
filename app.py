import os
import pandas as pd
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Python Analytics Server is running"}

# Existing MIS analytics endpoint
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

# 🔹 New endpoint for Analyze CSV (fixed file, same style as /mis)
@app.get("/analyze_csv")
def analyze_csv():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "students_analyze.csv")  # <--- place your CSV in the same folder

    df = pd.read_csv(csv_path)

    result = {
        "Average": float(df["Score"].mean()),
        "Highest": float(df["Score"].max()),
        "Lowest": float(df["Score"].min()),
        "FailureRate": float((df["Score"] < 60).mean() * 100.0)  # pass mark = 60
    }
    return result
