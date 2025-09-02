# config.py
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT

load_dotenv()

class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "CAMBIA_EN_PRODUCCION")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES") or 30)


    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "3306")
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_NAME: str = os.getenv("DB_NAME", "coworking_db")

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

settings = Settings()

# 🔑 Configuración específica para fastapi-jwt-auth
class AuthSettings(BaseModel):
    authjwt_secret_key: str = settings.SECRET_KEY
    authjwt_algorithm: str = settings.ALGORITHM

@AuthJWT.load_config
def get_config():
    return AuthSettings()
