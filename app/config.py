from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./wallet.db"
    APP_NAME: str = "Wallet API"

settings = Settings()
