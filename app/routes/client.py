from fastapi import APIRouter, HTTPException, Depends
from app.schemas import UserCreate, FileResponse
from app.models import User, users_db, UserRole
from app.utils.encryption import encrypt_filename
from app.utils.email_utils import send_mock_email
from app.auth import get_current_user, require_client_user, get_password_hash
import os

router = APIRouter()

UPLOAD_DIR = "uploads"

@router.post("/make-ops/{email}", tags=["Dev Only"])
def promote_user_to_ops(email: str):
    from app.models import users_db
    user = users_db.get(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.role = "ops"
    user.is_verified = True
    return {"message": f"{email} promoted to ops and verified ✅"}


@router.post("/signup/client", tags=["Client User"])
def signup_client(user: UserCreate):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = get_password_hash(user.password)
    users_db[user.email] = User(
        email=user.email,
        password_hash=hashed,
        is_verified=False,
        role=UserRole.CLIENT,
    )
    token = encrypt_filename(user.email)
    verify_url = f"/verify-email/{token}"
    send_mock_email(user.email, f"http://127.0.0.1:8000{verify_url}")
    return {"message": "User created. Check your email for verification.", "verify_url": verify_url}

@router.get("/verify-email/{token}", tags=["Client User"])
def verify_email(token: str):
    from app.utils.encryption import decrypt_filename
    try:
        email = decrypt_filename(token)
        user = users_db.get(email)
        if user:
            user.is_verified = True
            return {"message": "Email verified successfully"}
        raise HTTPException(status_code=404, detail="User not found")
    except:
        raise HTTPException(status_code=400, detail="Invalid verification link")

@router.get("/files", tags=["Client User"])
def list_uploaded_files(user: User = Depends(require_client_user)):
    files = os.listdir(UPLOAD_DIR)
    return {"files": files}

@router.get("/download-file/{filename}", tags=["Client User"], response_model=FileResponse)
def get_secure_download_link(filename: str, user: User = Depends(require_client_user)):
    from app.utils.encryption import encrypt_filename
    token = encrypt_filename(filename)
    return {
        "download_link": f"/secure-download/{token}",
        "message": "success"
    }

@router.get("/secure-download/{token}", tags=["Client User"])
def download_file(token: str, user: User = Depends(require_client_user)):
    from fastapi.responses import FileResponse
    from app.utils.encryption import decrypt_filename
    try:
        filename = decrypt_filename(token)
        path = os.path.join(UPLOAD_DIR, filename)
        if not os.path.exists(path):
            raise HTTPException(status_code=404, detail="File not found")
        return FileResponse(path, filename=filename)
    except:
        raise HTTPException(status_code=400, detail="Invalid or expired link")
