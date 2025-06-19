from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.models.Rules import Rules
from sqlalchemy import select
from pydantic import BaseModel
from app.models.FlightDetail import FlightDetail
import re
from app.models.Rules import Rules
from app.crud.airport import get_airport_name
from fastapi import HTTPException
from app.models.TicketClass import TicketClass
from sqlalchemy import func, select, join,and_, or_
from sqlalchemy.orm import selectinload


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
    
    
    
class FlightTransitOut(BaseModel):
    flight_route_id: Optional[str] = None
    transit_airport_name:Optional[str] = None
    stop_time: Optional[int] = None
    note: Optional[str] = None

async def get_transit_airport(db: AsyncSession) -> List[FlightTransitOut]:
    
    flight_detail = await db.execute(select(FlightDetail).options(selectinload(FlightDetail.transit_airport)))
    
    flight_details = flight_detail.scalars().all()
    result = []
    for fl in flight_details:
        result.append(FlightTransitOut(
            flight_route_id= fl.flight_route_id,
            transit_airport_name= fl.transit_airport.airport_name,
            stop_time= fl.stop_time,
            note= fl.note
        ))
    
    return result


async def generate_next_id(session):
    result = await session.execute(select(FlightDetail.flight_detail_id))
    ids = [row[0] for row in result.all()]

    max_num = 0
    for bid in ids:
        match = re.search(r'CTCB(\d+)', bid)
        if match:
            num = int(match.group(1))
            max_num = max(max_num, num)

    next_num = max_num + 1
    return f"CTCB{next_num:03d}" 


async def create_transit(input: FlightTransitOut, db: AsyncSession) -> Optional[FlightTransitOut]:
    rules = await db.execute(select(Rules))
    
    rules = rules.scalar()
    
    count_ = await db.execute(select(func.count(FlightDetail.flight_detail_id)).where(FlightDetail.flight_route_id == input.flight_route_id))
    
    count_ = count_.scalar()
    flight_detail_id = await generate_next_id(db)
    
    transit_airport = await get_airport_name(db,input.transit_airport_name)
    if transit_airport is None:
        raise HTTPException(status_code=404, detail=f"Airport '{input.transit_airport_name}' not exists")

    if count_ < rules.max_transit_airports:
        new_transit = FlightDetail(
            flight_detail_id = flight_detail_id,
            flight_route_id = input.flight_route_id,
            transit_airport_id = transit_airport.airport_id,
            stop_time = input.stop_time,
            note = input.note
        )
        
        db.add(new_transit)
        await db.commit()
        await db.refresh(new_transit)

        return FlightTransitOut(
            flight_route_id=new_transit.flight_route_id,
            transit_airport_name=input.transit_airport_name,
            stop_time=new_transit.stop_time,
            note=new_transit.note
        )
    else :
        raise HTTPException(status_code=400, detail= "Number of transit airports exceeds regulations")
    
    
    
    
class DeleteDetail(BaseModel):
    flight_route_id: Optional[str] = None
    transit_airport_name: Optional[str] = None
    
    
async def delete_transit(input: DeleteDetail, db: AsyncSession) -> str:
    
    transit = await db.execute(select(FlightDetail).options(selectinload(FlightDetail.transit_airport)).where(and_(
        FlightDetail.flight_route_id == input.flight_route_id,
        FlightDetail.transit_airport.has(airport_name=input.transit_airport_name)
    )))
    
    transit_airport = transit.scalar()
    if not transit_airport:
        raise HTTPException(status_code=404, detail="Transit airport not found")

    await db.delete(transit_airport)
    await db.commit()
    return "Deleted successfully"


class TicketClassCreate(BaseModel):
    ticket_class_id: Optional[str] = None
    ticket_class_name: Optional[str] = None
    
    
async def get_ticket_class(db: AsyncSession) -> List[TicketClass]:
    result = await db.execute(select(TicketClass))
    
    return result.scalars().all()

async def create_tkclass(input: TicketClassCreate, db: AsyncSession) -> Optional[TicketClass]:
    new_ticket_class = TicketClass(
        ticket_class_id=input.ticket_class_id,
        ticket_class_name=input.ticket_class_name
    )
    db.add(new_ticket_class)
    await db.commit()
    await db.refresh(new_ticket_class)
    return new_ticket_class