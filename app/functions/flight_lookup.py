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
from datetime import datetime, time, date, timedelta
from sqlalchemy import select, and_, or_
from app.models.Rules import Rules

class FlightSearch(BaseModel):
    flight_id: Optional[str] = None
    departure_address: Optional[str] = None
    departure_date: Optional[date] = None
    
    arrival_address: Optional[str] = None
    
    min_time: Optional[time] = None
    max_time: Optional[time] = None
    is_empty: Optional[bool] = False
    
    least_empty_seats: Optional[int] = None
    total_seats: Optional[int] = None



    
async def get_all_flights(db: AsyncSession, skip: int = 0, limit: int = 1000) -> List[Flight]:
    now = datetime.now()
    rules = await db.execute(select(Rules))
    rules = rules.scalar()
    latest_booking_delta = timedelta(hours=rules.latest_booking_time)

    
    result = await db.execute(select(Flight)
                              .options(
                                selectinload(Flight.flight_route)
                                .selectinload(FlightRoute.departure_airport),
                                selectinload(Flight.flight_route)
                                .selectinload(FlightRoute.arrival_airport),
                                selectinload(Flight.flight_route)
                                .selectinload(FlightRoute.flight_details)
                                .selectinload(FlightDetail.transit_airport),
                                selectinload(Flight.ticket_class_statistics)
                                .selectinload(TicketClassStatistics.ticket_class)
                                .selectinload(TicketClass.ticket_prices),
                              ).where(
                                  or_(Flight.flight_date > now.date(),
                                      and_(
                                        Flight.flight_date == now.date(),
                                        Flight.departure_time > (now - latest_booking_delta).time()
                                      ))
                              )
                              .offset(skip).limit(limit))
    
    return result.scalars().all()





async def find_flights_by_filter(db: AsyncSession,filters: FlightSearch, skip: int = 0, limit: int = 1000) -> List[Flight]:
    conditions = []
    
    now = datetime.now()
    rules = await db.execute(select(Rules))
    rules = rules.scalar()
    latest_booking_delta = timedelta(hours=rules.latest_booking_time)

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
        
    
    if filters.is_empty:
        conditions.append(Flight.ticket_class_statistics.any(TicketClassStatistics.available_seats > 0))
        
        
        
    query = (
        select(Flight)
        .join(Flight.flight_route)
        .join(FlightRoute.departure_airport)
        .options(
            selectinload(Flight.flight_route).selectinload(FlightRoute.departure_airport),
            selectinload(Flight.flight_route).selectinload(FlightRoute.arrival_airport),
            selectinload(Flight.flight_route).selectinload(FlightRoute.flight_details).selectinload(FlightDetail.transit_airport),
            selectinload(Flight.ticket_class_statistics).selectinload(TicketClassStatistics.ticket_class).selectinload(TicketClass.ticket_prices),        )
    )
    
    
    if conditions:
        query = query.where(and_(*conditions),
                            or_(Flight.flight_date > now.date(),
                                and_(
                                    Flight.flight_date == now.date(),
                                    Flight.departure_time > (now - latest_booking_delta).time()
                        )))
        
        
    query = query.offset(skip).limit(limit)    
    result = await db.execute(query)
    return result.scalars().all()