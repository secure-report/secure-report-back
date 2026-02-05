# ARCHIVO: secure-report-back/app/core/config.py
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Configuración centralizada de la aplicación"""
    
    MONGODB_URI: str
    MONGODB_DB_NAME: str = "securereport"
    APP_NAME: str = "SecureReport"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    # Cloudinary
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str
    
    # Google AI
    GOOGLE_API_KEY: str
    GOOGLE_MODEL: str = "gemini-2.5-flash"
    
    # Admin
    ADMIN_API_KEY: str

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()