# Step 1: FastAPI server to deploy on Railway

from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import FileResponse
import aiofiles
import os
import uuid

app = FastAPI()
UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def root():
    return {"message": "Server is running."}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

    return {"status": "uploaded", "file_path": filename}

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=filename, media_type='application/octet-stream')
    return {"error": "File not found"}
