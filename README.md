# Secure File Sharing System (FastAPI)

A RESTful API for secure file sharing between two types of users:
- **Ops User**: Can upload `.docx`, `.xlsx`, `.pptx` files
- **Client User**: Can sign up, verify email, login, and securely download files

## 🚀 Features

- ✅ JWT-based Auth for Clients & Ops
- ✅ Email verification with encrypted tokens
- ✅ Upload (restricted to specific types)
- ✅ Secure download links (tokenized & client-only)
- ✅ Swagger UI support

## 📁 Folder Structure

secure-share/
├── app/
│ ├── main.py
│ ├── auth.py
│ ├── models.py
│ ├── schemas.py
│ ├── database.py
│ ├── utils/
│ │ ├── encryption.py
│ │ └── email_utils.py
│ └── routes/
│ ├── ops.py
│ └── client.py
├── uploads/
├── requirements.txt
└── README.md

markdown
Copy code

## 🧪 API Testing Flow

1. `POST /signup/client` → Sign up client
2. `GET /verify-email/{token}` → Verify email
3. `POST /login` → Login & get JWT
4. Paste token in Swagger "Authorize" box
5. `POST /make-ops/{email}` (only if making Ops)
6. `POST /upload` → Upload file (only for Ops)
7. `GET /files` → List uploaded files (only for Clients)
8. `GET /download-file/{filename}` → Get secure link
9. `GET /secure-download/{token}` → Download securely

## 💡 Run the App

```bash
uvicorn app.main:app --reload
🧪 Run Tests
bash
Copy code
pytest test_main.py
📦 Dependencies
css
Copy code
fastapi
uvicorn
python-multipart
passlib[bcrypt]
python-jose
cryptography