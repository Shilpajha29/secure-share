from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.models import User, users_db, UserRole
from app.schemas import Token
from typing import Optional

router = APIRouter()

# JWT Config
SECRET_KEY = "your-secret-key-here"  # move to .env for production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ------------------------------
# Utils
# ------------------------------
def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_user(email: str) -> Optional[User]:
    return users_db.get(email)

# ------------------------------
# Routes
# ------------------------------
@router.post("/login", response_model=Token, tags=["Auth"])  
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# ------------------------------
# Dependency
# ------------------------------
def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(email)
    if user is None:
        raise credentials_exception
    return user

def require_ops_user(user: User = Depends(get_current_user)):
    if user.role != UserRole.OPS:
        raise HTTPException(status_code=403, detail="Only Ops users allowed")
    return user

def require_client_user(user: User = Depends(get_current_user)):
    if user.role != UserRole.CLIENT:
        raise HTTPException(status_code=403, detail="Only Client users allowed")
    return user
