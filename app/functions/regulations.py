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
from app.models.TicketPrice import TicketPrice
from app.models.Airport import Airport
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

    if count_ < rules.max_transit_airports and (input.stop_time <= rules.max_stop_time and input.stop_time >= rules.min_stop_time):
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
    
    return result.unique().scalars().all()

async def create_tkclass(input: TicketClassCreate, db: AsyncSession) -> Optional[TicketClass]:
    new_ticket_class = TicketClass(
        ticket_class_id=input.ticket_class_id,
        ticket_class_name=input.ticket_class_name
    )
    db.add(new_ticket_class)
    await db.commit()
    await db.refresh(new_ticket_class)
    return new_ticket_class

class TicketClassRoute(BaseModel):
    flight_route_id: Optional[str] = None
    ticket_class_name: Optional[str] = None
    price: Optional[int] = None
    
    
    
async def get_ticket_class_by_route(db: AsyncSession) -> List[TicketClassRoute]:
    result = await db.execute(select(TicketPrice).options(selectinload(TicketPrice.ticket_class)))
    
    results = result.scalars().all()

    ticket_class = []
    
    for result in results:
        ticket_class.append(TicketClassRoute(
            flight_route_id= result.flight_route_id,
            ticket_class_name= result.ticket_class.ticket_class_name,
            price = result.price
        ))


    return ticket_class

async def generate_ticket_price_id(session) -> str:
    result = await session.execute(select(TicketPrice.ticket_price_id))
    ids = [row[0] for row in result.fetchall() if row[0]]

    max_num = 0
    for bid in ids:
        match = re.search(r'DG(\d+)', bid)
        if match:
            try:
                num = int(match.group(1))
                max_num = max(max_num, num)
            except ValueError:
                continue  

    next_num = max_num + 1
    return f"DG{next_num:02d}" 


async def get_ticket_class_id_by_name(name: str, db: AsyncSession) -> str:
    result = await db.execute(
        select(TicketClass.ticket_class_id)
        .where(TicketClass.ticket_class_name == name)
    )
    ticket_class_id = result.scalar_one_or_none()

    if not ticket_class_id:
        raise HTTPException(status_code=404, detail=f"Ticket class '{name}' not exists.")

    return ticket_class_id

async def create_ticket_class_by_route(input: TicketClassRoute,db: AsyncSession) -> List[TicketClassRoute]:


    rules = await db.execute(select(Rules))
    
    rules = rules.scalar_one_or_none()  
    if not rules:
        raise HTTPException(status_code=404, detail="Rules not found")
            
    count_ = await db.execute(select(func.count(TicketPrice.ticket_class_id)).where(TicketPrice.flight_route_id == input.flight_route_id))

    if count_.scalar() < rules.ticket_class_count:

        ticket_class_id = await get_ticket_class_id_by_name(input.ticket_class_name, db)

        result = await db.execute(
            select(TicketPrice).where(
                TicketPrice.flight_route_id == input.flight_route_id,
                TicketPrice.ticket_class_id == ticket_class_id
            )
        )
        if result.scalar_one_or_none(): 
            raise HTTPException(status_code=400, detail="Ticket price exists")

        new_id = await generate_ticket_price_id(db)

        new_price = TicketPrice(
            ticket_price_id=new_id,
            flight_route_id=input.flight_route_id,
            ticket_class_id=ticket_class_id,
            price=input.price
        )
        db.add(new_price)
        await db.commit()
        await db.refresh(new_price)

        return TicketClassRoute(
            flight_route_id=input.flight_route_id,
            ticket_class_name=input.ticket_class_name,
            price=input.price
        )

    else:
        raise HTTPException(status_code=400, detail= "Ticket class in route is fully")



async def get_airport_name(db: AsyncSession, name: str) -> Optional[Airport]:
    result = await db.execute(
        select(Airport).where(Airport.airport_name == name)
    )
    return result.scalar_one_or_none()


async def update_transit(input: FlightTransitOut, db: AsyncSession) -> str:
    transit = await db.execute(
        select(FlightDetail)
        .options(selectinload(FlightDetail.transit_airport))
        .where(
            FlightDetail.flight_route_id == input.flight_route_id)
    )
    transit_detail = transit.scalar_one_or_none()

    if not transit_detail:
        raise HTTPException(status_code=404, detail="Transit airport not found")

    rules = (await db.execute(select(Rules))).scalar_one_or_none()
    if not rules:
        raise HTTPException(status_code=500, detail="Rules not found")

    if input.stop_time is not None:
        if input.stop_time < rules.min_stop_time or input.stop_time > rules.max_stop_time:
            raise HTTPException(status_code=400, detail=f"Stop time must be between {rules.min_stop_time} and {rules.max_stop_time} minutes")
        transit_detail.stop_time = input.stop_time

    if input.note is not None:
        transit_detail.note = input.note

        
    if input.transit_airport_name is not None:
        new_airport = await get_airport_name(db, input.transit_airport_name)
        if not new_airport:
            raise HTTPException(status_code=404, detail="New transit airport not found")
        transit_detail.transit_airport_id = new_airport.airport_id
        
    await db.commit()
    return "Transit updated successfully"

async def update_ticket_classs(input: TicketClassCreate, db: AsyncSession) -> str:
    if not input.ticket_class_id:
        raise HTTPException(status_code=400, detail="ticket_class_id is required")

    result = await db.execute(
        select(TicketClass).where(TicketClass.ticket_class_id == input.ticket_class_id)
    )
    ticket_class = result.scalar_one_or_none()

    if not ticket_class:
        raise HTTPException(status_code=404, detail="Ticket class not found")

    if input.ticket_class_name:
        ticket_class.ticket_class_name = input.ticket_class_name

    await db.commit()
    return "Ticket class updated successfully"

async def update_ticket_class_by_route(input: TicketClassRoute, db: AsyncSession) -> str:
    if not input.flight_route_id or not input.ticket_class_name:
        raise HTTPException(status_code=400, detail="Missing flight_route_id or ticket_class_name")

    new_ticket_class_id = await get_ticket_class_id_by_name(input.ticket_class_name, db)

    duplicate_check = await db.execute(
        select(TicketPrice).where(
            TicketPrice.flight_route_id == input.flight_route_id,
            TicketPrice.ticket_class_id == new_ticket_class_id
        )
    )
    if duplicate_check.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="This ticket class has already been added to the route.")

    current = await db.execute(
        select(TicketPrice)
        .where(TicketPrice.flight_route_id == input.flight_route_id)
        .limit(1)
    )
    ticket_price = current.scalar_one_or_none()

    if not ticket_price:
        raise HTTPException(status_code=404, detail="No ticket price entry found for update.")

    ticket_price.ticket_class_id = new_ticket_class_id
    if input.price is not None:
        ticket_price.price = input.price

    await db.commit()
    return "Ticket class and price updated successfully"



