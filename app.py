import os
import pandas as pd
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Python Analytics Server is running"}

@app.get("/mis")
def mis_analytics():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "test.csv")

    df = pd.read_csv(csv_path)

    result = {
        "Total": int(len(df)),
        "StudentID": df["StudentID"].value_counts().to_dict(),
        "Score": df["SCore"].value_counts().to_dict()
        #"employmentrate": float(df["employedwithin6months"].mean()),
        #"averagegpa": float(df["gpa"].mean())
    }
    return result
