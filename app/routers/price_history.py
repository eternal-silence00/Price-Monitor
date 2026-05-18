from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.repositories.price_history import PriceHistoryRepo

router = APIRouter()

@router.get("/price_history/{coin_id}")
async def get_price_history_by_coin_id(
    coin_id: str,
    limit: int = 10,
    offset: int = 0,
    session: AsyncSession = Depends(get_db)
):
    repo = PriceHistoryRepo(session)
    result = await repo.get_history_by_coin_id(coin_id, limit, offset)
    return result