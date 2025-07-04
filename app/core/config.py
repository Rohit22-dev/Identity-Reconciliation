import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings"""
    
    # Database
    DB_CONNECTION_STRING: str = os.getenv("DB_CONNECTION_STRING", "")
    
    # API Settings
    API_TITLE: str = "Bitespeed Identity Reconciliation"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "API for contact identity reconciliation and management"
    
    # CORS Settings
    CORS_ORIGINS: list = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: list = ["*"]
    CORS_HEADERS: list = ["*"]
    
    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True

# Global settings instance
settings = Settings() 