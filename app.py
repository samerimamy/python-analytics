from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Python Analytics Server is running"}

# 🔹 Just receive the CSV and return its name and size
@app.post("/analyze_csv")
async def analyze_csv(file: UploadFile = File(...)):
    content = await file.read()   # read all bytes
    return {
        "filename": file.filename,
        "size_bytes": len(content),
        "content_start": content[:100].decode("utf-8", errors="ignore")  # preview first 100 chars
    }
