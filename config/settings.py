from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "YummyGo"
    debug: bool = True
    database_url: str = "postgresql://username:password@localhost:5432/yummygo_db"
    secret_key: str = "your_secret_key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"  # Đọc từ file .env

settings = Settings()
