from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.tracking import Tracking

class TrackingRepo:
    
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_by_id(self, tracking_id: int):
        result = await self.session.execute(select(Tracking).where(Tracking.id == tracking_id))
        return result.scalar_one_or_none()
    
    async def get_all_users_trackings(self, user_id: int, limit: int = 10, offset: int = 0):
        result = await self.session.execute(select(Tracking).where(Tracking.user_id == user_id).limit(limit).offset(offset))
        return result.scalars().all()
    
    async def create_tracking(self, user_id: int, coin_id: str):
        tracking = Tracking(user_id=user_id, coin_id=coin_id)
        self.session.add(tracking)
        await self.session.flush()
        await self.session.refresh(tracking)
        return tracking
    
    async def delete_tracking(self, tracking_id):
        result = await self.session.execute(select(Tracking).where(Tracking.id == tracking_id))
        tracking = result.scalar_one_or_none()
        await self.session.delete(tracking)
        await self.session.flush()
        return 
    
    async def get_all_unique_coins(self):
        result = await self.session.execute(
        select(Tracking.coin_id).distinct()
        )
        return result.scalars().all()