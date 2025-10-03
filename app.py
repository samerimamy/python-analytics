from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/analyze_csv")
def analyze_csv():
    return {"message": "CSV endpoint is alive"}
