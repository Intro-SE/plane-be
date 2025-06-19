from app.schemas.Airport import AirportCreate, AirportInDB, AirportUpdate
from app.models.Airport import Airport
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import re
from typing import Optional, List
from app.models.Rules import Rules

async def get_all_airports(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Airport]:
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

    
async def create_airport(db: AsyncSession, airport: AirportCreate) -> Airport:
    airport_id = await generate_airport_id(db)
    
    rules = await db.execute(select(Rules))
    
    rules = rules.scalar()
    
    airports = await db.execute(select(func.count(Airport.airport_id)))
    
    
    if airports.scalar() < rules.max_airports:
        new_airport = Airport(
            airport_id=airport_id,
            airport_name=airport.airport_name,
            airport_address=airport.airport_address
        )
        db.add(new_airport)
        await db.commit()
        await db.refresh(new_airport)
        return new_airport
    else:
        raise ValueError("Number of airports exceeds regulations")


async def update_airport(db: AsyncSession, db_airport: Airport, airport: AirportUpdate) -> Airport:

    update_data = airport.dict(exclude_unset=True)
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