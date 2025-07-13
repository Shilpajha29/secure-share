from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from app.auth import require_ops_user
import os

router = APIRouter()

UPLOAD_DIR = "uploads"
ALLOWED_EXT = [".docx", ".pptx", ".xlsx"]

@router.post("/upload", tags=["Ops User"])
def upload_file(file: UploadFile = File(...), user=Depends(require_ops_user)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXT:
        raise HTTPException(status_code=400, detail="File type not allowed")
    with open(os.path.join(UPLOAD_DIR, file.filename), "wb") as f:
        f.write(file.file.read())
    return {"message": f"{file.filename} uploaded successfully"}
