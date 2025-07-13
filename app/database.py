from typing import Dict
from app.models import User

# In-memory "databases"
users_db: Dict[str, User] = {}
files_db: Dict[str, dict] = {}
