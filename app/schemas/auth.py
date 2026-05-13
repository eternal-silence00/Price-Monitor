from pydantic import BaseModel, ConfigDict

class UserCreate(BaseModel):
    email: str
    password: str
    
class UserResponse(BaseModel):
    id: int
    email: str
    
    model_config = ConfigDict(from_attributes=True)
    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
    model_config = ConfigDict(from_attributes=True)
    