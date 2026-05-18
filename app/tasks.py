from app.celery_app import celery_app
import asyncio
import requests
from app.database import AsyncSessionLocal
from app.repositories.tracking import TrackingRepo
from app.repositories.price_history import PriceHistoryRepo
from app.models.user import User
from app.models.tracking import Tracking
from app.models.price_history import PriceHistory

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"

@celery_app.task(max_retries = 3, default_retry_delay = 30)
def fetch_coin_price():
    asyncio.run(fetch_coin_price_async())
    
async def fetch_coin_price_async():
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker
    from app.config import settings
    
    engine = create_async_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with SessionLocal() as session:
        coins = await TrackingRepo(session).get_all_unique_coins()
        for coin in coins:
            try:
                response = requests.get(COINGECKO_URL, params={
                    "ids": coin,
                    "vs_currencies": "usd"
                })
                price = response.json()[coin]["usd"]
                await PriceHistoryRepo(session).create_price_record(coin, price)
            except Exception as e:
                print(f"Error fetching {coin}: {e}")
                continue
        await session.commit()
    await engine.dispose()
                
        