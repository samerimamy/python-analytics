from fastapi import FastAPI, Query
import os

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Python Analytics Server is running"}

@app.get("/show_file")
def show_file(filename: str = Query(..., description="File name to display")):
    if not os.path.exists(filename):
        return {"error": f"File not found: {filename}"}

    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return {"error": str(e)}

    # Only return the first 2000 characters to avoid overload
    preview = content[:2000] + ("..." if len(content) > 2000 else "")

    return {
        "filename": filename,
        "length": len(content),
        "preview": preview
    }
