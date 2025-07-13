# 🔐 Secure File Sharing System — FastAPI Based

This is a beginner-friendly full-stack FastAPI project that demonstrates how to securely share files between two different user types — **Ops Users** and **Client Users** — with email verification, JWT authentication, encrypted download URLs, and role-based access control.

---

##  Features

- ✅ Client User Sign-up with mock email verification
- ✅ JWT-based login for both Ops & Client users
- ✅ Role-based access:
  - **Only Ops** can upload files (.docx, .pptx, .xlsx)
  - **Only Clients** can list/download files via secure links
- ✅ Encrypted download URLs (Fernet) that restrict access by role
- ✅ Postman collection for testing
- ✅ Beginner-friendly codebase with clean folder structure

---

## 🧠 Tech Stack

- **Framework**: FastAPI
- **Auth**: OAuth2 + JWT tokens
- **Encryption**: `cryptography.fernet`
- **Data**: In-memory DB (for demo)
- **Test Tool**: Postman
- **Lang**: Python 3.10+

---

## 📁 Folder Structure
secure-share/
├── app/
│ ├── main.py # App entry
│ ├── auth.py # Login, JWT logic
│ ├── models.py # Data models
│ ├── schemas.py # Pydantic schemas
│ ├── database.py # In-memory user store
│ ├── utils/
│ │ ├── encryption.py # Fernet encrypt/decrypt
│ │ └── email_utils.py # Mock email sender
│ └── routes/
│ ├── ops.py # Upload route (only Ops)
│ └── client.py # Signup, download, etc.
├── uploads/ # Uploaded files
├── assets/ # Screenshot assets
├── .env # JWT_SECRET key
├── requirements.txt
├── README.md

---

## 🛠️ Getting Started

### 1. Clone & Setup
```bash
git clone https://github.com/YOUR_USERNAME/secure-share.git
cd secure-share
python -m venv venv
venv\Scripts\activate  # Or: source venv/bin/activate (Linux/Mac)
pip install -r requirements.txt
uvicorn app.main:app --reload

🧪 Testing Flow (Step-by-Step with Screenshots)

📝 Step 1: Sign Up (Client)
Endpoint: POST /signup/client

Creates a new client and sends a mock email link in console.


✅ Step 2: Email Verification
Copy the link shown in terminal and paste it in browser.


🔐 Step 3: Login
Use /login with form data (username, password)


📤 Step 4: Upload File (Only for Ops)
Endpoint: POST /upload

Only .docx, .xlsx, .pptx are allowed

Only JWT-authenticated Ops can access


📁 Step 5: List All Files (Client Only)
Endpoint: GET /files

Client can view list of all uploaded files.


🔗 Step 6: Generate Secure Download Link
Client can generate a Fernet-encrypted download URL.


💾 Step 7: Secure Download (Only Client Allowed)
Access the /secure-download/{token} URL

File will download

If Ops or invalid token: access is denied


🔐 Sample Users
Role	Email	Password
Ops	client1@example.com	abc123
Client	client2@example.com	abcabc

Use /login to get access token for either role.

📦 Postman Collection
✅ All endpoints are configured in:
secure-file-sharing.postman_collection.json

Just import into Postman and test one-by-one 🔁
