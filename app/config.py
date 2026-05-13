from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL:str
    REDIS_URL: str
    base_url: str = "http://localhost:8000"
    secret_key: str
    algorithm: str
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
        
    
        
settings = Settings()