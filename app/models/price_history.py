from sqlalchemy import Column, Integer, String,Float, TIMESTAMP
from app.models.base import Base
from datetime import datetime, timezone

class PriceHistory(Base):
    
    __tablename__ = "price_history"
    
    id = Column(Integer, primary_key=True)
    coin_id = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    

