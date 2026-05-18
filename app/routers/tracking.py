from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.repositories.tracking import TrackingRepo
from app.schemas.tracking import TrackingCreate, TrackingResponse
from app.services.auth import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/tracking")
async def get_all_trackings(
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user), 
    limit: int = 10,
    offset: int = 0
):
    repo = TrackingRepo(session)
    result = await repo.get_all_users_trackings(user.id, limit, offset)
    return result 

@router.get("/tracking/{tracking_id}")
async def get_tracking_by_id(
    tracking_id: int,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    repo = TrackingRepo(session)
    result = await repo.get_by_id(tracking_id)
    if not result: 
        raise HTTPException(status_code=404, detail="Tracking not found")
    if result.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
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
    return 
    
    