from sqlalchemy.ext.asyncio import AsyncSession
from app.models.Employee import Employee
from app.schemas.Employee import EmployeeCreate, EmployeeUpdate
from typing import Optional, List
from sqlalchemy.orm import selectinload,joinedload
from sqlalchemy import select, func
import re
from sqlalchemy.future import select
from app.core.security import get_password_hash
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await db.query(Employee).filter_by(employee_username=username).first()
    if not user:
        return None
    if not pwd_context.verify(password, user.employee_password):
        return None
    return user

async def get_by_id(db: AsyncSession, employee_id: str) -> Optional[Employee]:
    result = await db.execute(
        select(Employee)
        .options(joinedload(Employee.booking_tickets))
        .where(Employee.employee_id == employee_id)
    )
    return result.unique().scalars().one_or_none()

async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100)-> List[Employee]:
    result = await db.execute(select(Employee)
                            .options(selectinload(Employee.booking_tickets))
                            .offset(skip).limit(limit))
    return result.scalars().all()



async def generate_next_id(session):
    result = await session.execute(
        select(func.max(Employee.employee_id))
    )
    max_id = result.scalar()

    if not max_id:
        return "NV001"
    
    match = re.search(r'NV(\d+)', max_id)
    if match:
        next_num = int(match.group(1)) + 1
        return f"NV{next_num:02d}" 
    else:
        raise ValueError("Mã nhân viên hiện tại không đúng định dạng 'NVxxx'")
    
async def create(db: AsyncSession, obj_in: EmployeeCreate) -> Employee:
    new_id = await generate_next_id(db)  
    
    db_obj = Employee(
        employee_id=new_id,            
        **obj_in.dict(exclude={"employee_password"}),
        employee_password=get_password_hash(obj_in.employee_password)
    )
    
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def update(db: AsyncSession, db_obj: Employee, obj_in: EmployeeUpdate) -> Employee:
    update_data = obj_in.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_obj, field, value)

    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def remove(db: AsyncSession, employee_id: str) -> Optional[Employee]:
    obj = await get_by_id(db, employee_id)
    
    if obj:
        await db.delete(obj)
        await db.commit()
    return obj


async def get_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(Employee).where(Employee.employee_username == username))
    return result.scalars().first()