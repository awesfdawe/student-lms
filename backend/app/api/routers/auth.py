from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
import jwt
from app.core.config import settings
from app.core.security import (
    verify_password,
    create_access_token,
    create_temp_token,
    generate_totp_secret,
    verify_totp,
    get_totp_uri,
    generate_recovery_codes,
    get_password_hash
)
from app.core.email import send_email
from app.core.cache import get_redis
from app.crud.crud_user import get_user_by_email, create_user
from app.schemas.user import UserRead, UserRegister
from app.schemas.token import Token, TwoFactorRequired, TwoFactorVerify, TwoFactorSetup, TwoFactorCode, TwoFactorDisable
from app.api.deps import get_db, get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/register", response_model=UserRead)
async def register(user_in: UserRegister, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = await create_user(db=db, user_in=user_in)
    background_tasks.add_task(
        send_email,
        to=new_user.email,
        subject="Регистрация в Student LMS",
        body=f"Добро пожаловать! Ваш аккаунт {new_user.email} успешно создан.",
    )
    return new_user

@router.post("/login", response_model=Token | TwoFactorRequired)
async def login(db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user.is_2fa_enabled and user.totp_secret:
        temp_token = create_temp_token(data={"sub": user.email})
        return TwoFactorRequired(temp_token=temp_token)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token)

@router.post("/login/verify-2fa", response_model=Token)
async def verify_2fa(body: TwoFactorVerify, db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired temporary token",
    )
    try:
        payload = jwt.decode(body.temp_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "2fa_temp":
            raise credentials_exception
        email = payload.get("sub")
        if not email:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    r = get_redis()
    if r:
        attempts = await r.get(f"2fa_fail:{body.temp_token}")
        if attempts and int(attempts) >= 5:
            raise HTTPException(status_code=400, detail="Too many failed attempts")

    user = await get_user_by_email(db, email=email)
    if not user or not user.totp_secret:
        raise credentials_exception

    is_valid_totp = verify_totp(user.totp_secret, body.code)
    is_valid_recovery = False
    
    if not is_valid_totp and user.recovery_codes:
        new_codes = list(user.recovery_codes)
        for idx, hashed_code in enumerate(new_codes):
            if verify_password(body.code, hashed_code):
                is_valid_recovery = True
                new_codes.pop(idx)
                user.recovery_codes = new_codes
                await db.commit()
                break

    if not is_valid_totp and not is_valid_recovery:
        if r:
            await r.incr(f"2fa_fail:{body.temp_token}")
            await r.expire(f"2fa_fail:{body.temp_token}", 300)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid code",
        )

    if r:
        await r.delete(f"2fa_fail:{body.temp_token}")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token)

@router.post("/2fa/enable", response_model=TwoFactorSetup)
async def enable_2fa(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user.is_2fa_enabled:
        raise HTTPException(status_code=400, detail="2FA already enabled")
    secret = generate_totp_secret()
    codes = generate_recovery_codes()
    hashed_codes = [get_password_hash(c) for c in codes]
    current_user.totp_secret = secret
    current_user.recovery_codes = hashed_codes
    await db.commit()
    uri = get_totp_uri(secret, current_user.email)
    return TwoFactorSetup(secret=secret, otpauth_uri=uri, recovery_codes=codes)

@router.post("/2fa/confirm")
async def confirm_2fa(body: TwoFactorCode, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if not current_user.totp_secret:
        raise HTTPException(status_code=400, detail="Call /2fa/enable first")
    if not verify_totp(current_user.totp_secret, body.code):
        raise HTTPException(status_code=400, detail="Invalid TOTP code")
    current_user.is_2fa_enabled = True
    await db.commit()
    return {"status": "2fa_enabled"}

@router.post("/2fa/disable")
async def disable_2fa(body: TwoFactorDisable, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if not current_user.is_2fa_enabled:
        raise HTTPException(status_code=400, detail="2FA not enabled")
    if not verify_password(body.password, current_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    if not verify_totp(current_user.totp_secret, body.code):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid 2FA code")
    
    current_user.is_2fa_enabled = False
    current_user.totp_secret = None
    current_user.recovery_codes = None
    await db.commit()
    return {"status": "2fa_disabled"}
