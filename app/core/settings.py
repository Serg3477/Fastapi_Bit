from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    USER_DB_URL: str
    USER_DB_DIR: str
    HISTORY_DB_URL: str
    SECRET_KEY: str


    class Config:
        env_file = ".env"

settings = Settings()
