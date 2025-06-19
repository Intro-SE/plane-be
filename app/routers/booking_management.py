from sqlalchemy.ext.asyncio import AsyncSession
from app.models.BookingTicket import BookingTicket
from app.functions.booking_management import (
    get_all,delete ,BookingTicketOut, BookingCreate, 
    create, TicketSearch, search_by_filters, 
    update, BookingUpdate, export
)
from typing import Optional, List
from datetime import timedelta, date, time, datetime
from fastapi import APIRouter, HTTPException, status, Depends
from app.deps import get_db

router = APIRouter()


@router.get("/tickets", response_model=List[BookingTicketOut])
async def get_all_tickets(skip: int = 0, limit: int = 1000, db: AsyncSession = Depends(get_db)):
    try:
        tickets = await get_all(db,  skip, limit)
        
        result = []
        
        for ticket in tickets:
            
            ticket_class = ticket.ticket_class
            ticket_price = next(
                (price.price for price in ticket_class.ticket_prices
                    if price.flight_route_id == ticket.flight.flight_route_id),
                None
            ) 
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
                ticket_price = ticket_price,
                ticket_status = ticket.ticket_status,
                booking_date = datetime.now().date(),
                employee_id = ticket.employee.employee_id,
                employee_name= ticket.employee.employee_name
            )
            result.append(stat) 
            
        return result
    except Exception as e:
        raise HTTPException(status_code= 500, detail= str(e))
    
    
    
@router.post("/search_by_filters", response_model= List[BookingTicketOut])    
async def search_ticket_by_filters(filters: TicketSearch, skip: int = 0, limit: int = 1000 ,db: AsyncSession = Depends(get_db)):
    try:
        tickets = await search_by_filters(db, filters, skip, limit)
        
        result = []
        
        for ticket in tickets:
            
            ticket_class = ticket.ticket_class
            ticket_price = next(
                (price.price for price in ticket_class.ticket_prices
                    if price.flight_route_id == ticket.flight.flight_route_id),
                None
            ) 
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
                ticket_price = ticket_price,
                ticket_status = ticket.ticket_status,
                booking_date = datetime.now().date(),
                employee_id = ticket.employee.employee_id,
                employee_name= ticket.employee.employee_name
            )
            result.append(stat) 
            
        return result
    except Exception as e:
        raise HTTPException(status_code= 500, detail= str(e))

@router.post("/create", response_model= BookingTicketOut)
async def create_ticket(new_ticket: BookingCreate, db: AsyncSession = Depends(get_db)):
    try:
        ticket = await create(db, new_ticket)
        departure_date = ticket.flight.flight_date
        
        
        
        
        ticket_ = BookingTicketOut(
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
            ticket_price = ticket.booking_price,
            ticket_status = ticket.ticket_status,
            booking_date = datetime.now().date(),
            employee_id = ticket.employee.employee_id,
            employee_name= ticket.employee.employee_name
        )
        return ticket_
    except Exception as e:
        raise HTTPException(status_code= 500, detail= str(e))
        
        
@router.put("/update", response_model= BookingTicketOut)
async def update_ticket(update_ticket: BookingUpdate, db: AsyncSession = Depends(get_db)):
    
    try:
        ticket = await update(db, update_ticket)
        departure_date = ticket.flight.flight_date
        
        
        ticket_ = BookingTicketOut(
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
            ticket_price = ticket.booking_price,
            ticket_status = ticket.ticket_status,
            booking_date = datetime.now().date(),
            employee_id = ticket.employee.employee_id,
            employee_name= ticket.employee.employee_name
        )
        return ticket_
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
    

@router.delete("/delete")
async def delete_tickets(booking_ticket_ids: List[str], db: AsyncSession = Depends(get_db)):
    message = await delete(booking_ticket_ids, db)
    return {"log": message}

@router.patch("/export")
async def export_tickets(booking_ticket_ids: List[str], db: AsyncSession = Depends(get_db)):
    message = await export(booking_ticket_ids, db)
    return {"log" : message}
