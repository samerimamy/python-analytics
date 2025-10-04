import os
import pandas as pd
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Python Analytics Server is running"}

@app.get("/files")
def list_files():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return {"current_dir": base_dir, "files": os.listdir(base_dir)}


@app.get("/mis")
def mis_analytics():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "test.csv")

    df = pd.read_csv(csv_path)

    result = {
        "Total": int(len(df)),
        "BySemester": df["Semester"].value_counts().to_dict(),
        "ByCourse": df["Course"].value_counts().to_dict(),
        "EmploymentRate": float(df["EmployedWithin6Months"].mean()),
        "AverageGPA": float(df["GPA"].mean())
    }
    return result
