from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import secrets
import base64
import hashlib
import io
import jwt
import pyotp
import segno
from cryptography.fernet import Fernet, InvalidToken
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data, expires_delta=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_temp_token(data):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.TEMP_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "2fa_temp"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def generate_totp_secret():
    return pyotp.random_base32()


def verify_totp(secret, code):
    totp = pyotp.TOTP(secret)
    return totp.verify(code)


def generate_recovery_codes(count=10):
    return [secrets.token_hex(4) for _ in range(count)]


def get_totp_uri(secret, email):
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(name=email, issuer_name=settings.PROJECT_NAME)


def _get_fernet() -> Fernet:
    """Derive a Fernet key from the app's SECRET_KEY."""
    key = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(key))


def encrypt_totp_secret(secret: str) -> str:
    """Encrypt a TOTP secret before storing in DB."""
    f = _get_fernet()
    return f.encrypt(secret.encode()).decode()


def decrypt_totp_secret(encrypted: str) -> str:
    """Decrypt a TOTP secret from DB. Falls back to plaintext for migration."""
    f = _get_fernet()
    try:
        return f.decrypt(encrypted.encode()).decode()
    except (InvalidToken, Exception):
        return encrypted



def generate_qr_data_url(data: str) -> str:
    """Generate a QR code as a base64 SVG data URL (no external service)."""
    qr = segno.make(data)
    buffer = io.BytesIO()
    qr.save(buffer, kind="svg", xmldecl=False, svgns=False, scale=4)
    svg_bytes = buffer.getvalue()
    b64 = base64.b64encode(svg_bytes).decode()
    return f"data:image/svg+xml;base64,{b64}"
