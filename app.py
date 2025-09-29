from fastapi import FastAPI
import pandas as pd

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Python Analytics Server is running"}

@app.get("/mis")
def mis_analytics():
    df = pd.read_csv("students_mis.csv")  # Make sure the CSV is included

    result = {
        "Total": int(len(df)),
        "ByDepartment": df["Department"].value_counts().to_dict()
    }
    return result
