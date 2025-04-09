from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select, and_, func, select, or_
from app.models.staff import Account, StaffProfile, InternalStaff
from fastapi import HTTPException, status
from app.schemas.staff import InternalStaffResponse,StaffProfileFetch,StaffProfileSchema,StaffResponse 
from sqlalchemy.orm import selectinload

from app.schemas.staff import StaffCreate,InternalStaffCreate

from passlib.context import CryptContext

import app.schemas.staff as staffSchema

import uuid

import logging


logger = logging.getLogger("full_info")

role = ["staff"]

bcrypt_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")


async def get_all_staff(session: AsyncSession) -> list[StaffResponse]:
    staff = []
    
    result = await session.execute(
        select(StaffProfile)
        .options(
            selectinload(StaffProfile.account)
        )
        .limit(50)
    )
    staff = result.scalar().all()
    
    return staff

async def check_available_username(username: str, db_session :AsyncSession):
    return await InternalStaff.find(db_session,[InternalStaff.username == username])

async def create_internal_staff(user_data : InternalStaff, db_session: AsyncSession):
    account = InternalStaff(
        username = user_data.username,
        role = "staff",
        is_active = True,
        hassed_password = bcrypt_context.hash(user_data.password)
    )
    db_session.add(account)
    await db_session.commit()
    
    new_staff = InternalStaffResponse(
        id = account.id,
        first_name = user_data.first_name,
        last_name = user_data.last_name,
        email = user_data.email,
        username = user_data.username,
        role = ["staff"]
    )
    
    return new_staff

async def change_password(id : str, password : str,new_password :str, db_session: AsyncSession):
    staff_id = uuid.UUID(id)
    
    _staff : InternalStaff = await InternalStaff.find(
        db_session,[InternalStaff.id == staff_id]
    )
    if not bcrypt_context.verify(password,_staff.hashed_password):
        raise HTTPException(status_code=401, detail = "Error on pass change ")
    _staff.hashed_password = bcrypt_context.hash(new_password)
    await _staff.save(db_session)
    await db_session.commit()