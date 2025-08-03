from fastapi import APIRouter, Depends, HTTPException, status
from app.schema.user import UserCreate, Token, UserRead
from app.model.user import User
from app.db.session import async_session
from app.core.security import hash_password, verify_password, create_access_token, get_current_user
from sqlmodel import select

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(user_credentials: UserCreate):
    async with async_session() as session:
        query = select(User).where(User.username == user_credentials.username)
        result = await session.execute(query)
        user = result.scalar_one_or_none()

        if not user or not verify_password(user_credentials.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = create_access_token(
            data={"sub": user.username, "is_owner": user.is_owner}
        )
        return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserRead)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# @router.post("/register", response_model=UserRead)
# async def register(user_in: UserCreate):
#     async with async_session() as session:
#         # Vérifier si l'utilisateur existe déjà
#         query = select(User).where(User.username == user_in.username)
#         result = await session.execute(query)
#         existing_user = result.scalar_one_or_none()
#
#         if existing_user:
#             raise HTTPException(
#                 status_code=400,
#                 detail="Username already registered"
#             )
#
#         # Créer le nouvel utilisateur
#         hashed_password = hash_password(user_in.password)
#         db_user = User(
#             username=user_in.username,
#             hashed_password=hashed_password,
#             is_owner=False  # Par défaut, pas admin
#         )
#         session.add(db_user)
#         await session.commit()
#         await session.refresh(db_user)
#
#         return db_user
