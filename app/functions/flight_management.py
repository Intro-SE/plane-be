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
from pydantic import BaseModel
from datetime import datetime, time, date
from sqlalchemy import select, and_, or_
from app.functions.flight_lookup import FlightSearch



async def find_flights_by_filter(db: AsyncSession,filters: FlightSearch, skip: int = 0, limit: int = 100) -> List[Flight]:
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