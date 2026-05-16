from app.celery_app import celery_app
import asyncio
import requests
from app.database import AsyncSessionLocal
from app.repositories.tracking import TrackingRepo
from app.repositories.price_history import PriceHistoryRepo

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"

@celery_app.task(bind=True, max_retries = 3, default_retry_delay = 30)
def fetch_coin_price():
    asyncio.run(fetch_coin_price_async())
    
async def fetch_coin_price_async():
    async with AsyncSessionLocal() as session:
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
                
        