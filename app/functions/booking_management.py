from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from pydantic import BaseModel, validator, ValidationError
from typing import Optional, List
from app.models.BookingTicket import BookingTicket
from datetime import date, time, datetime,timedelta
from sqlalchemy.orm import selectinload
from app.models.Flight import Flight
from app.models.TicketClass import TicketClass
from app.crud.flight import get_id
from app.crud.booking_ticket import generate_next_id
from fastapi import HTTPException
from app.models.TicketClassStatistics import TicketClassStatistics
from app.models.TicketPrice import TicketPrice
from app.models.Employee import Employee
from app.models.FlightRoute import FlightRoute
import re
from sqlalchemy.exc import SQLAlchemyError
from app.models.Rules import Rules


class BookingTicketOut(BaseModel):
    booking_ticket_id: Optional[str] = None
    flight_id: Optional[str] = None
    flight_route_id: Optional[str] = None
    departure_date: Optional[date] = None
    arrival_date: Optional[date] = None
    flight_duration: Optional[int] = None
    
    departure_time: Optional[time] = None
    departure_airport: Optional[str] = None
    departure_name: Optional[str] = None
    departure_address: Optional[str] = None
    
    arrival_time: Optional[time] = None
    arrival_airport: Optional[str] = None
    arrival_name: Optional[str] = None
    arrival_address: Optional[str] = None
    
    passenger_name : Optional[str] = None
    national_id : Optional[str] = None
    passenger_gender : Optional[str] = None
    passenger_phone: Optional[str] = None

    ticket_class_id: Optional[str] = None
    ticket_class_name: Optional[str] = None
    ticket_price: Optional[int] = None
    ticket_status:Optional[bool] = None
    booking_date: Optional[date] = None
    employee_id: Optional[str] = None
    employee_name: Optional[str] = None
    
    
    
    
class TicketSearch(BaseModel):
    departure_address: Optional[str] = None
    arrival_address: Optional[str] = None
    booking_ticket_id: Optional[str] = None
    ticket_class_name: Optional[str] = None
    departure_date: Optional[date]= None
    flight_id: Optional[str] = None
    min_price: Optional[int] = None
    max_price: Optional[int] = None
    passenger_name: Optional[str] = None
    national_id: Optional[str] = None
    passenger_phone: Optional[str] = None
    
    
    
    
class BookingCreate(BaseModel):
    flight_id: Optional[str] = None
    passenger_name : Optional[str] = None
    national_id : Optional[str] = None
    passenger_gender : Optional[str] = None
    passenger_phone: Optional[str] = None
    ticket_class_id : Optional[str] = None
    ticket_class_name: Optional[str] = None
    booking_price:  Optional[int] = None
    
    employee_id: Optional[str] = None
    
    class Config:
        from_attributes = True
        
    @validator("national_id")
    def validate_national_id(cls,v):
        if v is None:
            return v
        if not re.fullmatch(r"^\d{9}$|^\d{12}$", v):
            raise ValidationError("national_id must be exactly 9 or 12 digits")
        
        return v


class BookingUpdate(BaseModel):
    flight_id: Optional[str] = None
    booking_ticket_id: Optional[str] = None
    passenger_name : Optional[str] = None
    national_id : Optional[str] = None
    passenger_gender : Optional[str] = None
    passenger_phone: Optional[str] = None
    ticket_class_id : Optional[str] = None
    ticket_class_name: Optional[str] = None
    booking_price:  Optional[int] = None
    
    employee_id: Optional[str] = None
    
    class Config:
        from_attributes = True
        
        
async def get_all(db: AsyncSession, skip: int = 0, limit: int = 1000) -> List[BookingTicket]:
    result = await db.execute(select(BookingTicket).where(BookingTicket.ticket_status == False)
                              .options(
                                  selectinload(BookingTicket.flight).selectinload(Flight.flight_route),
                                  selectinload(BookingTicket.ticket_class).selectinload(TicketClass.ticket_prices),
                                  selectinload(BookingTicket.employee)
                              ).offset(skip).limit(limit))
    
    return result.scalars().all()



async def search_by_filters(db: AsyncSession, filters: TicketSearch,skip: int = 0, limit: int = 1000) -> List[BookingTicket]:
    
    query = (select(BookingTicket).join(BookingTicket.flight).join(BookingTicket.ticket_class).where(BookingTicket.ticket_status == False)
                              .options(
                                  selectinload(BookingTicket.flight).selectinload(Flight.flight_route).selectinload(FlightRoute.departure_airport),
                                  selectinload(BookingTicket.flight).selectinload(Flight.flight_route).selectinload(FlightRoute.arrival_airport),
                                  selectinload(BookingTicket.ticket_class).selectinload(TicketClass.ticket_prices),
                                  selectinload(BookingTicket.employee)
                              ))
    
    
    conditions = []
    
    if filters.departure_address:
        conditions.append(
            BookingTicket.flight.has(
                Flight.flight_route.has(
                    FlightRoute.departure_airport.has(
                        airport_address = filters.departure_address
                    )
                )
            )
        )
        
    if filters.arrival_address:
        conditions.append(
            BookingTicket.flight.has(
                Flight.flight_route.has(
                    FlightRoute.arrival_airport.has(
                        airport_address = filters.arrival_address
                    )
                )
            )
        )
    
    
    if filters.booking_ticket_id:
        conditions.append(
            BookingTicket.booking_ticket_id == filters.booking_ticket_id
        )
        
    if filters.ticket_class_name:
        conditions.append(BookingTicket.ticket_class.has(
            ticket_class_name = filters.ticket_class_name
        ))
        
        
    if filters.departure_date:
        conditions.append(
            BookingTicket.flight.has(
                flight_date = filters.departure_date
            )
        )
        
    if filters.flight_id:
        conditions.append(
            BookingTicket.flight_id == filters.flight_id
        )

    
    if filters.min_price:
        conditions.append(
            BookingTicket.booking_price >= filters.min_price
        )

    if filters.max_price:
        conditions.append(
            BookingTicket.booking_price <= filters.max_price
        )
        
    if filters.passenger_name:
        conditions.append(
            BookingTicket.passenger_name == filters.passenger_name
        )

    if filters.national_id:
        conditions.append(
            BookingTicket.national_id == filters.national_id
        )
        
    if filters.passenger_phone:
        conditions.append(
            BookingTicket.phone_number == filters.passenger_phone
        )
        
        
    if conditions:
        query = query.where(and_(*conditions))
        
    result = await db.execute(query.offset(skip).limit(limit))
        
    return result.scalars().all()

async def create(db: AsyncSession, new_ticket: BookingCreate) -> Optional[BookingTicket]:
    
    flight = await get_id(db, new_ticket.flight_id)
    
    if not flight:
        raise HTTPException(status_code= 404, detail= "Flight not exists")
    
    
    result = await db.execute(select(TicketClassStatistics).join(TicketClassStatistics.flight).join(TicketClassStatistics.ticket_class)
                                                            .where(Flight.flight_route_id == flight.flight_route_id,
                                                                TicketClassStatistics.flight_id == new_ticket.flight_id,
                                                                  TicketClassStatistics.ticket_class_id == new_ticket.ticket_class_id,
))
    
    ticket_ = result.scalars().first()
    
    
    rules = await db.execute(select(Rules))
    
    rules = rules.scalar()
    
    now = datetime.now()
    latest_booking_delta = timedelta(hours=rules.latest_booking_time)
    flight_datetime = datetime.combine(flight.flight_date, flight.departure_time)
    booking_deadline = flight_datetime - latest_booking_delta
    
    if now < booking_deadline:
        
        if not ticket_:
            raise HTTPException(status_code=404, detail= "Ticket class not found ")
        
        if ticket_.available_seats <= 0:
            raise HTTPException(status_code= 400, detail= "No available seat in flight")
        if not ticket_.ticket_class.ticket_prices:
            raise HTTPException(status_code=400, detail="Ticket class has no price info")

        ticket_.available_seats -= 1
        ticket_.booked_seats += 1
        
        db.add(ticket_)
        await db.flush()
        
        booking_ticket_id = await generate_next_id(db)

        route_id = flight.flight_route_id
        
        price_result = await db.execute(
            select(TicketPrice.price).where(
                TicketPrice.flight_route_id == route_id,
                TicketPrice.ticket_class_id == new_ticket.ticket_class_id
            )
        )
        
        ticket_price = price_result.scalar_one_or_none()
        
        if ticket_price is None:
            raise HTTPException(status_code=400, detail="Ticket price not found for route and class")
        
        new_ticket.booking_price = ticket_price
        ticket = BookingTicket(
            booking_ticket_id = booking_ticket_id,
            flight_id = new_ticket.flight_id,
            passenger_name = new_ticket.passenger_name,
            national_id = new_ticket.national_id,
            gender = new_ticket.passenger_gender,
            phone_number = new_ticket.passenger_phone,
            ticket_class_id = new_ticket.ticket_class_id,
            booking_price = new_ticket.booking_price,
            booking_date = datetime.now().date(),
            ticket_status = False,
            
            employee_id = new_ticket.employee_id
        )

        print(ticket.booking_price)
        db.add(ticket)
        await db.commit()
        await db.refresh(ticket)
        return ticket

    else:
        raise HTTPException(status_code=400, detail="This flight is no longer available for booking")

async def update(db: AsyncSession, update_ticket: BookingUpdate) -> Optional[BookingTicket]:
    
    ticket = await db.execute(select(BookingTicket)
                              .where(BookingTicket.booking_ticket_id == update_ticket.booking_ticket_id,
                                     )
                              .options(
                                  selectinload(BookingTicket.flight).selectinload(Flight.flight_route),
                                  selectinload(BookingTicket.ticket_class).selectinload(TicketClass.ticket_prices),
                                  selectinload(BookingTicket.employee),
                              ))
    
    ticket = ticket.scalar_one_or_none()

    price_result = await db.execute(
        select(TicketPrice.price).join(TicketPrice.flight_route).join(FlightRoute.flights).where(
            Flight.flight_id == update_ticket.flight_id,
            TicketPrice.ticket_class_id == update_ticket.ticket_class_id
        )
    )
    

    ticket_price = price_result.scalar_one_or_none()
    
    if ticket_price is None:
        raise HTTPException(status_code=400, detail="Ticket price not found for route and class")
    
    employee = await db.execute(select(Employee.employee_id).join(Employee.booking_tickets).where(BookingTicket.booking_ticket_id == update_ticket.booking_ticket_id))

    employee_id = employee.scalar_one_or_none()
    if employee_id is None:
        raise HTTPException(status_code= 400, detail= "Employee id not found")
    
    update_ticket.employee_id = employee_id
    update_ticket.booking_price = ticket_price

    if not ticket:
        raise HTTPException(status_code= 404, detail= "Ticket not found ")
    update_ticket.booking_price = ticket.booking_price
    
    ticket.flight_id = update_ticket.flight_id
    ticket.passenger_name = update_ticket.passenger_name
    ticket.national_id = update_ticket.national_id
    ticket.gender = update_ticket.passenger_gender
    ticket.phone_number = update_ticket.passenger_phone
    ticket.ticket_class_id = update_ticket.ticket_class_id
    ticket.booking_price = update_ticket.booking_price
    
    ticket.employee_id = update_ticket.employee_id
    await db.commit()
    await db.refresh(ticket)


    return ticket
    
    
    
async def delete(booking_ticket_ids : List[str], db: AsyncSession) -> str:
    try :
        result = await db.execute(select(BookingTicket).where(BookingTicket.booking_ticket_id.in_(booking_ticket_ids)))
        tickets = result.unique().scalars().all()
        
        if not tickets:
            raise HTTPException(status_code= 404, detail= "Tickets not exist")
        rules_result = await db.execute(select(Rules))
        
        rules = rules_result.scalar_one_or_none()
        if not rules:
            raise HTTPException(status_code=404, detail="Rules not found")

        now = datetime.now()
        latest_cancel_delta = timedelta(hours=rules.latest_cancel_time)
        
        for ticket in tickets:
            flight_result = await db.execute(
                select(Flight).where(Flight.flight_id == ticket.flight_id)
            )
            flight = flight_result.scalar_one_or_none()
            if not flight:
                raise HTTPException(status_code=404, detail="Flight not found for ticket")

            flight_datetime = datetime.combine(flight.flight_date, flight.departure_time)
            cancel_deadline = flight_datetime - latest_cancel_delta

            if now > cancel_deadline:
                raise HTTPException(
                    status_code=400,
                    detail=f"Cannot cancel ticket {ticket.booking_ticket_id}: past cancellation deadline"
                )
                
            stat = await db.execute(select(TicketClassStatistics)
                                    .where(
                                        TicketClassStatistics.flight_id == ticket.flight_id,
                                        TicketClassStatistics.ticket_class_id == ticket.ticket_class_id
                                    ))
            
            stat_ = stat.scalar_one_or_none()
            if stat_:
                stat_.available_seats += 1
                stat_.booked_seats -= 1
            await db.delete(ticket)
            
        await db.commit()
        
        return "Delete Successfully"
    
    except SQLAlchemyError as e:
        await db.rollback()
        return f"Delete Failed: {str(e)}"
    
    
async def export(booking_ticket_ids : List[str], db: AsyncSession) -> str:
    try :
        result = await db.execute(select(BookingTicket).where(BookingTicket.booking_ticket_id.in_(booking_ticket_ids)))
        tickets = result.unique().scalars().all()
        
        if not tickets:
            raise HTTPException(status_code= 404, detail= "Tickets not exist")

        now = datetime.now()

        for ticket in tickets:   
            flight_result = await db.execute(
                select(Flight).where(Flight.flight_id == ticket.flight_id)
            )
            flight = flight_result.scalar_one_or_none()
            if not flight:
                raise HTTPException(
                    status_code=404,
                    detail=f"Flight not found for ticket {ticket.booking_ticket_id}"
                )

            flight_datetime = datetime.combine(flight.flight_date, flight.departure_time)

            if now >= flight_datetime:
                raise HTTPException(
                    status_code=400,
                    detail=f"Cannot export ticket {ticket.booking_ticket_id}: Flight already departed"
                )

            ticket.ticket_status = True
            
        await db.commit()
        
        return "Export Successfully"

    except SQLAlchemyError as e:
        await db.rollback()
        return f"Export Failed: {str(e)}"