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
from datetime import date

class PriceInformation(BaseModel):
    min_price: Optional[int] = -1
    max_price: Optional[int] = -1

class FlightSearchInput(BaseModel):
    flight_id: Optional[str] = None
    departure_address: Optional[str] = None
    departure_date: Optional[date] = None
    arrival_address: Optional[str] = None
    arrival_date: Optional[date] = None
    price_information: Optional[PriceInformation] = None
    
    
async def get_all_flights(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Flight]:
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
                              ).offset(skip).limit(limit))
    
    return result.scalars().all()



