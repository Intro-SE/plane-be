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
    
    
class RulesUpdate(BaseModel):
    airport_number: Optional[int] = None
    min_flight_duration: Optional[int] = None
    max_stop_number: Optional[int] = None
    min_stop_duration: Optional[int] = None
    max_stop_duration: Optional[int] = None
    latest_time_to_book: Optional[int] = None
    latest_time_to_cancel: Optional[int] = None
    ticket_class_number: Optional[int] = None
    
    
async def get_rules(db: AsyncSession)-> Optional[RulesOut]:
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
    

async def update_rules(rules_input: RulesUpdate, db: AsyncSession) -> Optional[RulesOut]:
    query = (select(Rules))
    
    result = await db.execute(query)
    
    rules: Optional[Rules] = result.scalar_one_or_none()

    if rules is None:
        return None

    field_map = {
        "airport_number": "max_airports",
        "min_flight_duration": "min_flight_time",
        "max_stop_number": "max_transit_airports",
        "min_stop_duration": "min_stop_time",
        "max_stop_duration": "max_stop_time",
        "latest_time_to_book": "latest_booking_time",
        "latest_time_to_cancel": "latest_cancel_time",
        "ticket_class_number": "ticket_class_count"
    }

    for pydantic_field, orm_field in field_map.items():
        value = getattr(rules_input, pydantic_field)
        if value is not None:
            setattr(rules, orm_field, value)

    await db.commit()
    await db.refresh(rules)

    return RulesOut(
        airport_number=rules.max_airports,
        min_flight_duration=rules.min_flight_time,
        max_stop_number=rules.max_transit_airports,
        min_stop_duration=rules.min_stop_time,
        max_stop_duration=rules.max_stop_time,
        latest_time_to_book=rules.latest_booking_time,
        latest_time_to_cancel=rules.latest_cancel_time,
        ticket_class_number=rules.ticket_class_count
    )