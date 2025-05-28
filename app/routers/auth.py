from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.deps import get_db
from app.crud.taikhoannhanvien import get_by_username
from app.core.security import verify_password, create_access_token
from datetime import timedelta
from pydantic import BaseModel
from passlib.exc import UnknownHashError
from app.core.security import get_password_hash
router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 60

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/login", response_model=LoginResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user = await get_by_username(db, form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tên đăng nhập hoặc mật khẩu không đúng",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        if not verify_password(form_data.password, user.matkhau):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Tên đăng nhập hoặc mật khẩu không đúng",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except UnknownHashError:
        if form_data.password != user.matkhau:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Tên đăng nhập hoặc mật khẩu không đúng",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user.matkhau = get_password_hash(form_data.password)
        db.add(user)
        try:
            await db.commit()
            await db.refresh(user)
        except Exception as e:
            print(f"Lỗi khi cập nhật mật khẩu hash: {e}")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.tendangnhap}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
async def logout():
    return {"msg": "Logout thành công"}