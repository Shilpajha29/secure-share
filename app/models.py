from enum import Enum
from pydantic import BaseModel
from typing import Dict

class UserRole(str, Enum):
    CLIENT = "client"
    OPS = "ops"

class User(BaseModel):
    email: str
    password_hash: str
    is_verified: bool = False
    role: UserRole

# In-memory user storage (mock DB)
users_db: Dict[str, User] = {}
