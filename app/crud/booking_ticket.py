from app.models.BookingTicket import BookingTicket
from app.models.Flight import Flight
from app.models.FlightRoute import FlightRoute
from app.schemas.BookingTicket import BookingTicketCreate, BookingTicketUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.future import select
from typing import List
from datetime import datetime
from sqlalchemy import func
import re
from typing import Optional

async def get_all_tickets(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[BookingTicket]:
    result = await db.execute(
        select(BookingTicket)
        .options(
            joinedload(BookingTicket.ticket_class),
            joinedload(BookingTicket.employee),
            joinedload(BookingTicket.flight)
                .joinedload(Flight.flight_route)
                .joinedload(FlightRoute.departure_airport),
            joinedload(BookingTicket.flight)
                .joinedload(Flight.flight_route)
                .joinedload(FlightRoute.arrival_airport)
        )
        .offset(skip).limit(limit)
    )
    return result.unique().scalars().all()


async def get_id(db: AsyncSession, booking_ticket_id: str) -> Optional[BookingTicket]:
    result = await db.execute(select(BookingTicket).where(BookingTicket.booking_ticket_id == booking_ticket_id))
    return result.unique().scalars().one_or_none()



async def generate_next_id(session):
    result = await session.execute(select(BookingTicket.booking_ticket_id))
    ids = [row[0] for row in result.all()]

    max_num = 0
    for bid in ids:
        match = re.search(r'PDC(\d+)', bid)
        if match:
            num = int(match.group(1))
            max_num = max(max_num, num)

    next_num = max_num + 1
    return f"PDC{next_num:04d}" 
    
async def create_ticket(db: AsyncSession, ticket: BookingTicketCreate) -> BookingTicket:
    booking_ticket_id = await generate_next_id(db)
    new_ticket = BookingTicket(
        booking_ticket_id = booking_ticket_id,
        flight_id=ticket.flight_id,
        passenger_name=ticket.passenger_name,
        national_id=ticket.national_id,
        gender=ticket.gender,
        phone_number=ticket.phone_number,
        ticket_class_id=ticket.ticket_class_id,
        booking_price=ticket.booking_price,
        ticket_status=ticket.ticket_status,
        employee_id=ticket.employee_id,
        booking_date=datetime.now()
    )
    db.add(new_ticket)
    await db.commit()
    await db.refresh(new_ticket)
    return new_ticket


async def update_ticket(db: AsyncSession, db_ticket: BookingTicket, ticket: BookingTicketUpdate) -> BookingTicket:

    update_data = ticket.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_ticket, key, value)

    await db.commit()
    await db.refresh(db_ticket)
    return db_ticket

async def delete_ticket(db: AsyncSession,  obj_in: BookingTicket) -> Optional[BookingTicket]:
    if obj_in:
        await db.delete(obj_in)
        await db.commit()
    return obj_in