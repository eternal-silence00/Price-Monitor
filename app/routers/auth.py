from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.auth import hash_password, verify_password, create_access_token
from app.schemas.auth import UserCreate, UserResponse, TokenResponse
from app.repositories.user import UserRepo

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    data: UserCreate,
    session: AsyncSession = Depends(get_db)
):
    repo = UserRepo(session)
    user_exsists = await repo.get_by_email(data.email)
    if user_exsists:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_password = hash_password(data.password)
    user = await repo.create_user(data.email, hashed_password)
    return user
@router.post("/login", response_model=TokenResponse, status_code=200)
async def login(
    data: UserCreate,
    session: AsyncSession = Depends(get_db)
):
    repo = UserRepo(session)
    user = await repo.get_by_email(data.email)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    verified = verify_password(data.password, user.hashed_password)
    if not verified:
        raise HTTPException(status_code=400, detail="Wrong password")
    token = create_access_token({"sub":str(user.id)})
    return {"access_token":token, "token_type":"bearer"}