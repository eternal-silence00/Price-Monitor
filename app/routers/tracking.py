from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.repositories.tracking import TrackingRepo
from app.schemas.tracking import TrackingCreate, TrackingResponse
from app.services.auth import get_current_user
from app.models.user import User
from app.redis_client import redis_client
import json

router = APIRouter()


@router.get("/tracking")
async def get_all_trackings(
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user), 
    limit: int = 10,
    offset: int = 0
):
    cache_key = f"tracking:{user.id}:{limit}:{offset}"
    cached = await redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    repo = TrackingRepo(session)
    result = await repo.get_all_users_trackings(user.id, limit, offset)
    await redis_client.set(cache_key, json.dumps([{"id": t.id, "user_id": t.user_id, "coin_id": t.coin_id} for t in result]), ex=300)
    return result 

@router.get("/tracking/{tracking_id}")
async def get_tracking_by_id(
    tracking_id: int,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    cache_key = f"tracking:{tracking_id}"
    cached = await redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    repo = TrackingRepo(session)
    result = await repo.get_by_id(tracking_id)
    if not result: 
        raise HTTPException(status_code=404, detail="Tracking not found")
    if result.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    await redis_client.set(cache_key, json.dumps({"id":result.id, "user_id":result.user_id, "coin_id":result.coin_id}), ex=300)
    return result

@router.post("/tracking", response_model=TrackingResponse, status_code=201)
async def create_tracking(
    data: TrackingCreate,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    repo = TrackingRepo(session)
    tracking = await repo.create_tracking(
        user_id=user.id,
        coin_id=data.coin_id
    )
    keys = await redis_client.keys(f"tracking:{user.id}:*")
    if keys:
        await redis_client.delete(*keys)
    return tracking

@router.delete("/tracking/{tracking_id}")
async def delete_tracking(
    tracking_id: int,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    repo = TrackingRepo(session)
    tracking = await repo.get_by_id(tracking_id)
    if not tracking:
        raise HTTPException(status_code=404, detail="Tracking not found")
    if tracking.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    await repo.delete_tracking(tracking.id)
    keys = await redis_client.keys(f"tracking:{user.id}:*")
    if keys:
        await redis_client.delete(*keys)
    await redis_client.delete(f"tracking:{tracking_id}")
    return 
    
    