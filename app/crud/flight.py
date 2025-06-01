from app.schemas.Flight import FlightCreate, FlightUpdate
from app.models.Flight import Flight
from sqlalchemy.ext.asyncio import AsyncSession


from app.models.TicketClassStatistics import TicketClassStatistics
from app.models.FlightRoute import FlightRoute
from app.models.Flight import Flight
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload
import re
from typing import Optional, List
from datetime import datetime
from sqlalchemy import func

async def get_id(db: AsyncSession, flight_id: str) -> Optional[Flight]:
    result = await db.execute(select(Flight).where(Flight.flight_id == flight_id))
    return result.unique().scalars().one_or_none()

async def get_all_flight(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Flight]:
    result = await db.execute( select(Flight)
    .options(
        selectinload(Flight.flight_route)
        .selectinload(FlightRoute.departure_airport),
        selectinload(Flight.flight_route)
        .selectinload(FlightRoute.arrival_airport),
        selectinload(Flight.ticket_class_statistics).selectinload(TicketClassStatistics.ticket_class),
    )
    .offset(skip)
    .limit(limit))
    
    return result.unique().scalars().all()


async def generate_next_id(session):
    result = await session.execute(
        select(func.max(Flight.flight_id))
    )
    max_id = result.scalar()

    if not max_id:
        return "CB01"
    
    match = re.search(r'CB(\d+)', max_id)
    if match:
        next_num = int(match.group(1)) + 1
        return f"CB{next_num:02d}" 

    
async def create_flight(db: AsyncSession, flight: FlightCreate) -> Flight:
    
    flight_id = await generate_next_id(db)
    
    
    new_flight = Flight(
        flight_id = flight_id,
        flight_route_id= flight.route_id,
        departure_date= flight.departure_date,
        departure_time=flight.departure_time,
        duration= flight.duration,
        total_seats=flight.total_seats,
    )
    db.add(new_flight)
    await db.commit()
    await db.refresh(new_flight)
    return new_flight


async def update_flight(db: AsyncSession, db_flight: Flight, flight: FlightUpdate) -> Flight:

    update_data = flight.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_flight, key, value)

    await db.commit()
    await db.refresh(db_flight)
    return db_flight

async def delete_flight(db: AsyncSession,  obj_in: Flight) -> Optional[Flight]:
    if obj_in:
        await db.delete(obj_in)
        await db.commit()
    return obj_in