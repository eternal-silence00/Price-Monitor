from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Tracking(Base):
   
   __tablename__ = "tracking"
   
   id = Column(Integer, primary_key=True)
   user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
   coin_id = Column(String, nullable=False) #coin name ("Bitcoin" etc.)
   
   user = relationship("User", back_populates="tracking")