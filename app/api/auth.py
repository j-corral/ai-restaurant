from fastapi import APIRouter, HTTPException
from app.db.session import async_session
from app.core.security import verify_password, create_access_token
from sqlmodel import select

from app.model.user import User
from app.schema.user import Token, UserCreate

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(form_data: UserCreate):
    async with async_session() as session:
        query = select(User).where(User.username == form_data.username)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Wrong credentials")
        access_token = create_access_token({"sub": user.username, "is_owner": user.is_owner})
        return Token(access_token=access_token, token_type="bearer")
