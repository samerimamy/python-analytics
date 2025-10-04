from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Python Analytics Server is running"}

@app.get("/show_file")
def show_file(filename: str = "test.py"):
    if not os.path.exists(filename):
        return {"error": f"File not found: {filename}"}

    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return {"error": str(e)}

    # Return the whole file as plain text
    return {"filename": filename, "content": content}
