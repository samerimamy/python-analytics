from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Python Analytics Server is running"}

# 🔹 This is the only analyze_csv endpoint (must be POST)
@app.post("/analyze_csv")
async def analyze_csv(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8", errors="ignore")

    return {
        "filename": file.filename,
        "size_bytes": len(content),
        "preview": text[:100]  # just return first 100 chars
    }
