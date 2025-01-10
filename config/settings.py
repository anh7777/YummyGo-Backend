from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Tải các biến môi trường từ file .env
load_dotenv()

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    debug: bool = True

settings = Settings()  # Không cần env_file trong Config nữa
