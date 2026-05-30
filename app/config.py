from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL:str
    REDIS_URL: str
    base_url: str = "http://localhost:8000"
    secret_key: str
    algorithm: str
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM:str
    MAIL_SERVER:str
    MAIL_PORT:int
    
    model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    extra="ignore"
)
        
    
        
settings = Settings()