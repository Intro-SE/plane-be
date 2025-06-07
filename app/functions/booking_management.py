from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel
from typing import Optional, List
from app.models.Booking_Ticket import BookingTicket
from datetime import date, time, datetime
from sqlalchemy.orm import selectinload
from app.models.Flight import Flight
from app.models.TicketClass import TicketClass
from app.crud.flight import get_id
from app.crud.booking_ticket import generate_next_id
from fastapi import HTTPException
from app.models.TicketClassStatistics import TicketClassStatistics


class BookingTicketOut(BaseModel):
    booking_ticket_id: Optional[str] = None
    flight_id: Optional[str] = None
    flight_route_id: Optional[str] = None
    departure_date: Optional[date] = None
    arrival_date: Optional[date] = None
    flight_duration: Optional[int] = None
    
    departure_time: Optional[time] = None
    departure_airport: Optional[str] = None
    departure_name: Optional[str] = None
    departure_address: Optional[str] = None
    
    arrival_time: Optional[time] = None
    arrival_airport: Optional[str] = None
    arrival_name: Optional[str] = None
    arrival_address: Optional[str] = None
    
    passenger_name : Optional[str] = None
    national_id : Optional[str] = None
    passenger_gender : Optional[str] = None
    passenger_phone: Optional[str] = None

    ticket_class_id: Optional[str] = None
    ticket_class_name: Optional[str] = None
    ticket_price: Optional[int] = None
    ticket_status:Optional[bool] = None
    booking_date: Optional[date] = None
    employee_id: Optional[str] = None
    
    
    
class BookingCreate(BaseModel):
    flight_id: Optional[str] = None
    passenger_name : Optional[str] = None
    national_id : Optional[str] = None
    passenger_gender : Optional[str] = None
    passenger_phone: Optional[str] = None
    ticket_class_id : Optional[str] = None
    ticket_class_name: Optional[str] = None
    ticket_price:  Optional[int] = None
    
    employee_id: Optional[str] = None

async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[BookingTicket]:
    result = await db.execute(select(BookingTicket)
                              .options(
                                  selectinload(BookingTicket.flight).selectinload(Flight.flight_route),
                                  selectinload(BookingTicket.ticket_class).selectinload(TicketClass.ticket_prices),
                                  selectinload(BookingTicket.employee)
                              ).offset(skip).limit(limit))
    
    return result.scalars().all()



async def create(db: AsyncSession, new_ticket: BookingCreate) -> Optional[BookingTicket]:
    
    flight = await get_id(db, new_ticket.flight_id)
    
    if not flight:
        raise HTTPException(status_code= 404, detail= "Flight not exists")
    
    
    result = await db.execute(select(TicketClassStatistics)
                                    .options(
                                        selectinload(TicketClassStatistics.ticket_class).selectinload(TicketClass.ticket_prices),
                                        selectinload(TicketClassStatistics.flight)
                                    ).where(TicketClass.ticket_class_id == new_ticket.ticket_class_id,
                                            TicketClassStatistics.flight_id == new_ticket.flight_id))
    
    ticket_class = result.scalars().first()
    
    if not ticket_class:
        raise HTTPException(status_code=404, detail= "Ticket class not found ")
    
    
    ticket_class.available_seats -= 1
    ticket_class.booked_seats += 1
    ticket_price = ticket_class.ticket_class.ticket_prices[0].price
    booking_ticket_id = await generate_next_id(db)
    
    ticket = BookingTicket(
        booking_ticket_id = booking_ticket_id,
        flight_id = new_ticket.flight_id,
        passenger_name = new_ticket.passenger_name,
        national_id = new_ticket.national_id,
        gender = new_ticket.passenger_gender,
        phone_number = new_ticket.passenger_phone,
        ticket_class_id = new_ticket.ticket_class_id,
        booking_price = ticket_price,
        booking_date = datetime.now().date(),
        ticket_status = False,
        
        employee_id = new_ticket.employee_id
    )
    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)
    return ticket
    