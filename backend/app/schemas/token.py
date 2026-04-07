from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TwoFactorRequired(BaseModel):
    requires_2fa: bool = True
    temp_token: str

class TwoFactorVerify(BaseModel):
    temp_token: str
    code: str

class TwoFactorCode(BaseModel):
    code: str

class TwoFactorSetup(BaseModel):
    secret: str
    otpauth_uri: str
    recovery_codes: list[str]

class TwoFactorDisable(BaseModel):
    password: str
    code: str
