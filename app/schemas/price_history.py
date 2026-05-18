from pydantic import BaseModel, ConfigDict
from datetime import datetime

class PriceHistoryCreate(BaseModel):
    coin_id: str
    price: float
    
class PriceHistoryResponse(BaseModel):
    id: int
    coin_id: str
    price: float
    timestamp: datetime
    
    model_config = ConfigDict(from_attributes=True)