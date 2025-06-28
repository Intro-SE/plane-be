from app.schemas.Airport import AirportCreate, AirportInDB, AirportUpdate
from app.models.Airport import Airport
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
import re
from typing import Optional, List
from app.models.Rules import Rules
from fastapi import HTTPException

async def get_all_airports(db: AsyncSession, skip: int = 0, limit: int = 1000) -> List[Airport]:
    result = await db.execute(select(Airport).offset(skip).limit(limit))
    
    return result.scalars().all()

async def generate_airport_id(session):
    result = await session.execute(select(func.max(Airport.airport_id)))
    
    max_id = result.scalar()
    if not max_id:
        return "SB01"
    
    match = re.search(r'SB(\d+)',max_id)
    if match: 
        next_id = int(match.group(1)) + 1
        return f"SB{next_id:02d}"


async def get_id(db: AsyncSession, airport_id: str) -> Optional[Airport]:
    result = await db.execute(select(Airport).where(Airport.airport_id == airport_id))
    return result.unique().scalars().one_or_none()


async def get_airport_name(db: AsyncSession, airport_name: str) -> Optional[Airport]:
    result = await db.execute(select(Airport).where(Airport.airport_name == airport_name))
    return result.scalar()


async def create_airport(db: AsyncSession, airport: AirportCreate) -> Airport:
    airport_id = await generate_airport_id(db)

    # Lấy quy định hệ thống
    rules_result = await db.execute(select(Rules))
    rules = rules_result.scalar()

    # Đếm số lượng sân bay hiện tại
    airports_result = await db.execute(select(func.count(Airport.airport_id)))
    current_airports = airports_result.scalar()

    # Kiểm tra trùng tên và địa chỉ (không phân biệt hoa thường)
    duplicate_check = await db.execute(
        select(Airport).where(
            and_(
                func.lower(Airport.airport_name) == airport.airport_name.lower(),
                func.lower(Airport.airport_address) == airport.airport_address.lower()
            )
        )
    )
    existing_airport = duplicate_check.scalar_one_or_none()

    if existing_airport:
        raise ValueError("An airport with the same name and address already exists.")

    if current_airports >= rules.max_airports:
        raise ValueError("Number of airports exceeds regulations.")

    # Tạo sân bay mới
    new_airport = Airport(
        airport_id=airport_id,
        airport_name=airport.airport_name,
        airport_address=airport.airport_address
    )
    db.add(new_airport)
    await db.commit()
    await db.refresh(new_airport)
    return new_airport


async def update_airport(db: AsyncSession, db_airport: Airport, airport: AirportUpdate) -> Airport:
    update_data = airport.dict(exclude_unset=True)

    # Nếu cập nhật tên hoặc địa chỉ thì mới cần kiểm tra trùng
    new_name = update_data.get("airport_name", db_airport.airport_name)
    new_address = update_data.get("airport_address", db_airport.airport_address)

    # Kiểm tra trùng tên và địa chỉ với sân bay khác (không phân biệt hoa thường)
    result = await db.execute(
        select(Airport)
        .where(func.lower(Airport.airport_name) == new_name.lower())
        .where(func.lower(Airport.airport_address) == new_address.lower())
        .where(Airport.airport_id != db_airport.airport_id)  # Loại trừ chính nó
    )
    existing_airport = result.scalar_one_or_none()
    if existing_airport:
        raise HTTPException(
            status_code=400,
            detail="An airport with the same name and address already exists."
        )

    # Thực hiện cập nhật
    for key, value in update_data.items():
        setattr(db_airport, key, value)

    await db.commit()
    await db.refresh(db_airport)
    return db_airport

async def delete_airport(db: AsyncSession,  obj_in: Airport) -> Optional[Airport]:
    if obj_in:
        await db.delete(obj_in)
        await db.commit()
    return obj_in