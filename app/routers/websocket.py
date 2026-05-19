from fastapi import WebSocket, APIRouter, Depends
from app.database import get_db
from app.repositories.price_history import PriceHistoryRepo
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio

router = APIRouter()

@router.websocket("/ws/{coin_id}")
async def websocket_endpoint(coin_id: str, websocket: WebSocket,session:AsyncSession = Depends(get_db)):
    await websocket.accept()
    repo = PriceHistoryRepo(session)
    try:
        while True:
            result = await repo.get_latest_price(coin_id)
            await websocket.send_json({"coin_id": result.coin_id, "price": result.price})
            await asyncio.sleep(60)
    except Exception:
        await websocket.close()
    