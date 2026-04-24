from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Student LMS API"
    
    POSTGRES_SERVER: str = "127.0.0.1"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "student_lms"
    POSTGRES_PORT: int = 5432

    SECRET_KEY: str = "super_secret_key_change_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 240
    TEMP_TOKEN_EXPIRE_MINUTES: int = 5

    DIRECTUS_URL: str = ""
    DIRECTUS_API_KEY: str = ""

    VALKEY_HOST: str = "localhost"
    VALKEY_PORT: int = 6379
    VALKEY_DB: int = 0
    WEBHOOK_SECRET: str = ""

    S3_ENDPOINT: str = "http://127.0.0.1:8333"
    S3_ACCESS_KEY: str = "admin"
    S3_SECRET_KEY: str = "admin"
    S3_BUCKET: str = "directus"
    S3_REGION: str = "us-east-1"

    SMTP_HOST: str = "127.0.0.1"
    SMTP_PORT: int = 1025
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = "noreply@student-lms.local"

    @property
    def valkey_url(self):
        return f"redis://{self.VALKEY_HOST}:{self.VALKEY_PORT}/{self.VALKEY_DB}"

    @property
    def sqlalchemy_database_uri(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        case_sensitive=True, 
        extra='ignore'
    )

settings = Settings()
