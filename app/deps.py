from app.databases.session import async_session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.employee import get_by_username
from app.core.security import decode_access_token

async def get_db():
    async with async_session() as session:
        yield session
        

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    username = decode_access_token(token)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ hoặc hết hạn",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await get_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User không tồn tại")
    return user
