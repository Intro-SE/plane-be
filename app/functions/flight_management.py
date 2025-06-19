from app.models.Flight import Flight
from app.models.FlightRoute import FlightRoute
from app.models.FlightDetail import FlightDetail
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.TicketClassStatistics import TicketClassStatistics
from app.models.FlightRoute import FlightRoute
from app.models.TicketClass import TicketClass
from pydantic import BaseModel, validator
from datetime import datetime, time, date
from sqlalchemy import select, and_, or_, func
from app.functions.flight_lookup import FlightSearch
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import re


    
async def generate_next_id(session):
    result = await session.execute(select(TicketClassStatistics.ticket_class_statistics_id))
    ids = [row[0] for row in result.all()]

    max_num = 0
    for bid in ids:
        match = re.search(r'TK(\d+)', bid)
        if match:
            num = int(match.group(1))
            max_num = max(max_num, num)

    next_num = max_num + 1
    return f"TK{next_num:03d}" 

class FlightCreate(BaseModel):
    flight_id : Optional[str] = None
    flight_route: Optional[str] = None
    departure_airport: Optional[str] = None
    arrival_airport: Optional[str] = None
    departure_date: Optional[date] = None
    departure_time : Optional[time] = None
    flight_duration: Optional[int] = None
    total_seats: Optional[int] = None
    
    seat_type : Optional[List[str]] = None
    empty_type_seats: Optional[List[int]] = None
    
    
    class Config:
        from_attributes = True
    
    @validator('empty_type_seats')
    def check_logic_seats(cls, v ,values):
        if 'total_seats' in values and sum(v) != values['total_seats']:
            raise ValueError("Not enough total seats")
        return v

async def find_flights_by_filter(db: AsyncSession,filters: FlightSearch, skip: int = 0, limit: int = 1000) -> List[Flight]:
    conditions = []
    
    
    if filters.flight_id:
        conditions.append(Flight.flight_id == filters.flight_id)
        
        
        
    if filters.departure_address:
        conditions.append(
            Flight.flight_route.has(
                FlightRoute.departure_airport.has(
                    airport_address = filters.departure_address
                )
            )
        )
        
        
    if filters.arrival_address:
        conditions.append(
            Flight.flight_route.has(
                FlightRoute.arrival_airport.has(
                    airport_address = filters.arrival_address
                )
            )
        )
        
    if filters.departure_date:
        conditions.append(
            Flight.flight_date == filters.departure_date
        )
        
    if filters.min_time:
        conditions.append(Flight.departure_time >= filters.min_time)
        
    if filters.max_time:
        conditions.append(Flight.departure_time <= filters.max_time)
        
    if filters.least_empty_seats:
        conditions.append(
            Flight.ticket_class_statistics.any(
                TicketClassStatistics.available_seats >= filters.least_empty_seats
            )
        )
    
    if filters.total_seats:
        conditions.append(Flight.flight_seat_count >= filters.total_seats)
        
        
    if filters.is_empty:
        conditions.append(Flight.ticket_class_statistics.any(TicketClassStatistics.available_seats > 0))
        
        
        
    query = (
        select(Flight)
        .join(Flight.flight_route)
        .join(FlightRoute.departure_airport)
        .options(
            selectinload(Flight.flight_route).selectinload(FlightRoute.departure_airport),
            selectinload(Flight.flight_route).selectinload(FlightRoute.departure_airport),
            selectinload(Flight.flight_route).selectinload(FlightRoute.flight_details).selectinload(FlightDetail.transit_airport),
            selectinload(Flight.ticket_class_statistics).selectinload(TicketClassStatistics.ticket_class).selectinload(TicketClass.ticket_prices),        )
    )
    
    
    if conditions:
        query = query.where(and_(*conditions))
        
        
    query = query.offset(skip).limit(limit)    
    result = await db.execute(query)
    return result.scalars().all()




async def create_new_flight(db: AsyncSession, flight : FlightCreate) -> Flight:
    result=await  db.execute(select(FlightRoute).where(FlightRoute.flight_route_id == flight.flight_route)
                             .options(
                                 selectinload(FlightRoute.departure_airport),
                                 selectinload(FlightRoute.arrival_airport),
                                 selectinload(FlightRoute.flight_details),
                             ))
    
    route = result.unique().scalar_one_or_none()
    
    if not route:
        raise HTTPException(status_code= 404, detail= "Flight route not found")
    
    flight.departure_airport = route.departure_airport.airport_name
    flight.arrival_airport = route.arrival_airport.airport_name
    
    check = await db.execute(select(Flight).where(Flight.flight_id == flight.flight_id))
    
    if check.scalar_one_or_none():
        raise HTTPException(status_code= 400, detail= "Flight already exists")
    
    new_flight = Flight(
        flight_id = flight.flight_id,
        flight_route_id = flight.flight_route,
        flight_date = flight.departure_date,
        departure_time = flight.departure_time,
        flight_duration = flight.flight_duration,
        flight_seat_count = flight.total_seats
    )
    
    db.add(new_flight)
    
    for type_name, empty_seat in zip(flight.seat_type, flight.empty_type_seats):
        result  = await db.execute(select(TicketClass).where(TicketClass.ticket_class_name == type_name))
        ticket_class = result.unique().scalar_one_or_none()
        if not ticket_class:
            raise HTTPException(status_code=404, detail=f"Ticket class'{type_name}' not exists")
        ticket_class_statistics_id = await generate_next_id(db)
        stats = TicketClassStatistics(
            ticket_class_statistics_id = ticket_class_statistics_id,
            flight_id = flight.flight_id,
            ticket_class_id = ticket_class.ticket_class_id,
            total_seats = flight.total_seats,
            available_seats = empty_seat,
            booked_seats = 0
        )
        db.add(stats)
        
    await db.commit()
    result = await db.execute(
        select(Flight)
        .where(Flight.flight_id == flight.flight_id)
        .options(
            selectinload(Flight.flight_route).selectinload(FlightRoute.departure_airport),
            selectinload(Flight.flight_route).selectinload(FlightRoute.arrival_airport),
            selectinload(Flight.flight_route).selectinload(FlightRoute.flight_details).selectinload(FlightDetail.transit_airport),
            selectinload(Flight.ticket_class_statistics).selectinload(TicketClassStatistics.ticket_class).selectinload(TicketClass.ticket_prices)
        )
    )
    
    refreshed_flight = result.unique().scalar_one()
    return refreshed_flight





async def update_flight(db: AsyncSession, flight: FlightCreate) -> Flight:
    
    result = await db.execute(select(Flight).where(Flight.flight_id == flight.flight_id)
                              .options(
                                  selectinload(Flight.flight_route).selectinload(FlightRoute.departure_airport),
                                  selectinload(Flight.flight_route).selectinload(FlightRoute.arrival_airport),
                                  selectinload(Flight.ticket_class_statistics).selectinload(TicketClassStatistics.ticket_class)
                              ))
    exist_flight = result.unique().scalar_one_or_none()
    if not exist_flight:
        raise HTTPException(status_code= 404, detail= "Flight not exists")
    
    
    exist_flight.flight_route_id = flight.flight_route
    exist_flight.flight_date = flight.departure_date
    exist_flight.departure_time = flight.departure_time
    exist_flight.flight_duration = flight.flight_duration
    exist_flight.flight_seat_count = flight.total_seats
    
    flight.departure_airport = exist_flight.flight_route.departure_airport.airport_name
    flight.arrival_airport = exist_flight.flight_route.arrival_airport.airport_name

    await db.execute(TicketClassStatistics.__table__.delete().where(TicketClassStatistics.flight_id == flight.flight_id))
    
    
    for type_name, empty_seat in zip(flight.seat_type, flight.empty_type_seats):
        result = await db.execute(select(TicketClass).where(TicketClass.ticket_class_name == type_name))
        
        ticket_class = result.unique().scalar_one_or_none()
        
        if not ticket_class:
            raise HTTPException(status_code=404, detail= f"Ticket class {type_name} not exists")
        ticket_class_statistics_id = await generate_next_id(db)
        stats = TicketClassStatistics(
            ticket_class_statistics_id = ticket_class_statistics_id,
            flight_id = flight.flight_id,
            ticket_class_id = ticket_class.ticket_class_id,
            total_seats = flight.total_seats,
            available_seats = empty_seat,
            booked_seats = 0
        )
        db.add(stats)
        
    await db.commit()
    result = await db.execute(
        select(Flight)
        .where(Flight.flight_id == flight.flight_id)
        .options(
            selectinload(Flight.flight_route).selectinload(FlightRoute.departure_airport),
            selectinload(Flight.flight_route).selectinload(FlightRoute.arrival_airport),
            selectinload(Flight.flight_route).selectinload(FlightRoute.flight_details).selectinload(FlightDetail.transit_airport),
            selectinload(Flight.ticket_class_statistics).selectinload(TicketClassStatistics.ticket_class).selectinload(TicketClass.ticket_prices)
        )
    )
    
    refreshed_flight = result.unique().scalar_one()
    return refreshed_flight
    
    
    
async def delete_flight(flight_ids: List[str], db: AsyncSession) -> Optional[Flight]:
    try :
        result = await db.execute(select(Flight).where(Flight.flight_id.in_(flight_ids)))
        flights = result.scalars().all()
        
        if not flights:
            raise HTTPException(status_code= 404, detail= "Flights not exist")
        
        for flight in flights:
            await db.delete(flight)
            
        await db.commit()
        
        return "Delete Successfully"
    
    except SQLAlchemyError as e:
        await db.rollback()
        return f"Delete Failed: {str(e)}"