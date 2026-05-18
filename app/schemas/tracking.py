from pydantic import BaseModel, ConfigDict

class TrackingCreate(BaseModel):
    coin_id: str
    
class TrackingResponse(BaseModel):
    id: int
    user_id: int
    coin_id: str
    
    model_config = ConfigDict(from_attributes=True)
    