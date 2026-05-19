from fastapi import FastAPI
from app.database import engine
from contextlib import asynccontextmanager
from app.routers import auth, tracking, price_history, websocket

@asynccontextmanager
async def lifespan(app:FastAPI):
    yield
    await engine.dispose()
    
app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(tracking.router)
app.include_router(price_history.router)
app.include_router(websocket.router)