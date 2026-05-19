from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.repositories.price_history import PriceHistoryRepo
from app.redis_client import redis_client
import json

router = APIRouter()

@router.get("/price_history/{coin_id}/latest")
async def get_latest_coin_price(
    coin_id: str,
    session: AsyncSession = Depends(get_db)
):
    repo = PriceHistoryRepo(session)
    result = await repo.get_latest_price(coin_id)
    if not result:
        raise HTTPException(status_code=404, detail="price not found")
    return result


@router.get("/price_history/{coin_id}")
async def get_price_history_by_coin_id(
    coin_id: str,
    limit: int = 10,
    offset: int = 0,
    session: AsyncSession = Depends(get_db)
):
    cache_key = f"price_history:{coin_id}:{limit}:{offset}"
    cached = await redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    repo = PriceHistoryRepo(session)
    result = await repo.get_history_by_coin_id(coin_id, limit, offset)
    if not result:
        raise HTTPException(status_code=404, detail="Tracking not found")
    await redis_client.set(cache_key, json.dumps([{"id":t.id, "coin_id": t.coin_id, "price": t.price, "timestamp": str(t.timestamp)} for t in result]), ex=300)
    return result