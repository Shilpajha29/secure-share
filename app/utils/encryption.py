from cryptography.fernet import Fernet

FERNET_KEY = b'OmfApEjEC903g-j1loiCMdo2EUg3mLDO00j0otSKKc8='
fernet = Fernet(FERNET_KEY)


def encrypt_filename(filename: str) -> str:
    return fernet.encrypt(filename.encode()).decode()

def decrypt_filename(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()
