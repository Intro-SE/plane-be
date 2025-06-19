from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.models.Rules import Rules
from sqlalchemy import select
from pydantic import BaseModel

class RulesOut(BaseModel):
    airport_number: Optional[int] = None
    min_flight_duration: Optional[int] = None
    max_stop_number: Optional[int] = None
    min_stop_duration: Optional[int] = None
    max_stop_duration: Optional[int] = None
    latest_time_to_book: Optional[int] = None
    latest_time_to_cancel: Optional[int] = None
    ticket_class_number: Optional[int] = None
    
async def get_rules(db: AsyncSession)-> Optional[Rules]:
    query = (select(Rules))
    
    result = await db.execute(query)
    
    rules = result.scalar()
    
    
    return RulesOut(
        airport_number= rules.max_airports,
        min_flight_duration= rules.min_flight_time,
        max_stop_number= rules.max_transit_airports,
        min_stop_duration= rules.min_stop_time,
        max_stop_duration= rules.max_stop_time,
        latest_time_to_book= rules.latest_booking_time,
        latest_time_to_cancel= rules.latest_cancel_time,
        ticket_class_number= rules.ticket_class_count
    )