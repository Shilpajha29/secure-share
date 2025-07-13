from app.models import users_db

email = "ops1@example.com"

if email in users_db:
    users_db[email].role = "ops"
    users_db[email].is_verified = True
    print(f"{email} promoted to Ops and verified ✅")
else:
    print(f"{email} not found in users_db ❌")
