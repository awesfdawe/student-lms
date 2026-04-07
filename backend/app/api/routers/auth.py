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
)
from app.core.email import send_email
from app.crud.crud_user import get_user_by_email, create_user
from app.schemas.user import UserRead, UserRegister
from app.schemas.token import Token, TwoFactorRequired, TwoFactorVerify, TwoFactorSetup, TwoFactorCode
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

    user = await get_user_by_email(db, email=email)
    if not user or not user.totp_secret:
        raise credentials_exception

    if not verify_totp(user.totp_secret, body.code):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid TOTP code",
        )

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
    current_user.totp_secret = secret
    await db.commit()
    uri = get_totp_uri(secret, current_user.email)
    return TwoFactorSetup(secret=secret, otpauth_uri=uri)


@router.post("/2fa/confirm")
async def confirm_2fa(body: TwoFactorCode, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if not current_user.totp_secret:
        raise HTTPException(status_code=400, detail="Call /2fa/enable first")
    if not verify_totp(current_user.totp_secret, body.code):
        raise HTTPException(status_code=400, detail="Invalid TOTP code")
    current_user.is_2fa_enabled = True
    await db.commit()
    return {"status": "2fa_enabled"}
