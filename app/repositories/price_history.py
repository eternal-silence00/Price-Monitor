from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.price_history import PriceHistory

class PriceHistoryRepo:
    
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_history_by_coin_id(self, coin_id: str, limit: int = 10, offset: int = 0):
        result = await self.session.execute(select(PriceHistory).where(PriceHistory.coin_id == coin_id).limit(limit).offset(offset))
        return result.scalars().all()
    
    async def create_price_record(self, coin_id: str, price: float):
        record = PriceHistory(coin_id=coin_id, price=price)
        self.session.add(record)
        await self.session.flush()
        await self.session.refresh(record)
        return record
        
    async def get_previous_price(self, coin_id: str):
        result = await self.session.execute(
            select(PriceHistory)
            .where(PriceHistory.coin_id == coin_id)
            .order_by(PriceHistory.timestamp.desc())
            .offset(1)
            .limit(1)
        )
        return result.scalar_one_or_none()
    
    async def get_latest_price(self, coin_id: str):
        result = await self.session.execute(
            select(PriceHistory)
            .where(PriceHistory.coin_id == coin_id)
            .order_by(PriceHistory.timestamp.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()