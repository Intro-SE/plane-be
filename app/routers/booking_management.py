from sqlalchemy.ext.asyncio import AsyncSession
from app.models.Booking_Ticket import BookingTicket
from app.functions.booking_management import get_all, BookingTicketOut, BookingCreate, create

from typing import Optional, List
from datetime import timedelta, date, time, datetime
from fastapi import APIRouter, HTTPException, status, Depends
from app.deps import get_db

router = APIRouter()


@router.get("/", response_model= List[BookingTicketOut])
async def get_all_tickets(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    try:
        tickets = await get_all(db, skip, limit)
        result = []
        for ticket in tickets:
            departure_date = ticket.flight.flight_date
            stat = BookingTicketOut(
                booking_ticket_id = ticket.booking_ticket_id,
                flight_id = ticket.flight_id,
                flight_route_id = ticket.flight.flight_route_id,
                departure_date = ticket.flight.flight_date,
                arrival_date = departure_date + timedelta(minutes = ticket.flight.flight_duration),
                flight_duration = ticket.flight.flight_duration,
                
                departure_time = ticket.flight.departure_time,
                departure_airport = ticket.flight.flight_route.departure_airport_id,
                departure_name = ticket.flight.flight_route.departure_airport.airport_name,
            
                departure_address = ticket.flight.flight_route.departure_airport.airport_address,
                
                arrival_time = (datetime.combine(ticket.flight.flight_date, ticket.flight.departure_time)+ timedelta(minutes=ticket.flight.flight_duration)).time(),
                arrival_airport = ticket.flight.flight_route.arrival_airport_id,
                arrival_name= ticket.flight.flight_route.arrival_airport.airport_name,
                arrival_address = ticket.flight.flight_route.arrival_airport.airport_address,
                
                passenger_name = ticket.passenger_name,
                national_id = ticket.national_id,
                passenger_gender = ticket.gender,
                passenger_phone = ticket.phone_number,

                ticket_class_id = ticket.ticket_class.ticket_class_id,
                ticket_class_name = ticket.ticket_class.ticket_class_name,
                ticket_price = ticket.ticket_class.ticket_prices[0].price,
                ticket_status = ticket.ticket_status,
                booking_date = datetime.now().date(),
                employee_id = ticket.employee.employee_id
            )
            result.append(stat)
            
        return result
    except Exception as e:
        raise  HTTPException(status_code= 500, detail= str(e))
    
@router.post("/create", response_model= BookingCreate)
async def create_ticket(new_ticket: BookingCreate, db: AsyncSession = Depends(get_db)) -> Optional[BookingTicket]:
    
    ticket = await create(db, new_ticket)
    departure_date = ticket.flight.flight_date
    stat = BookingTicketOut(
        booking_ticket_id = ticket.booking_ticket_id,
        flight_id = ticket.flight_id,
        flight_route_id = ticket.flight.flight_route_id,
        departure_date = ticket.flight.flight_date,
        arrival_date = departure_date + timedelta(minutes = ticket.flight.flight_duration),
        flight_duration = ticket.flight.flight_duration,

        departure_time = ticket.flight.departure_time,
        departure_airport = ticket.flight.flight_route.departure_airport_id,
        departure_name = ticket.flight.flight_route.departure_airport.airport_name,

        departure_address = ticket.flight.flight_route.departure_airport.airport_address,

        arrival_time = (datetime.combine(ticket.flight.flight_date, ticket.flight.departure_time)+ timedelta(minutes=ticket.flight.flight_duration)).time(),
        arrival_airport = ticket.flight.flight_route.arrival_airport_id,
        arrival_name= ticket.flight.flight_route.arrival_airport.airport_name,
        arrival_address = ticket.flight.flight_route.arrival_airport.airport_address,

        passenger_name = ticket.passenger_name,
        national_id = ticket.national_id,
        passenger_gender = ticket.gender,
        passenger_phone = ticket.phone_number,

        ticket_class_id = ticket.ticket_class.ticket_class_id,
        ticket_class_name = ticket.ticket_class.ticket_class_name,
        ticket_price = ticket.ticket_class.ticket_prices[0].price,
        ticket_status = ticket.ticket_status,
        booking_date = datetime.now().date(),
        employee_id = ticket.employee.employee_id
    )
    return stat
        