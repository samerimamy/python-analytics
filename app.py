import os
import pandas as pd
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Python Analytics Server is running"}

@app.get("/mis")
def aaa():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "students_mis.csv")

    df = pd.read_csv(csv_path)

    result = {
        "BySemester": df["Semester"].value_counts().to_dict(),
        "Total": int(len(df)),
        "ByCourse": df["Course"].value_counts().to_dict(),
        "EmploymentRate": float(df["EmployedWithin6Months"].mean()),
        "AverageGPA": float(df["GPA"].mean())
    }
    return result
#@app.get("/analyze_csv")
# # def analyze_csv_analytics():
    # # base_dir = os.path.dirname(os.path.abspath(__file__))
    # # csv_path = os.path.join(base_dir, "students_mis.csv")

    # # df = pd.read_csv(csv_path)

    # # result = {
        # # print(df.to_dict(orient="records"))
    # # }
    # # return result
