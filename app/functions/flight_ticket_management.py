from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import Optional, List
from app.models.BookingTicket import BookingTicket
from datetime import date, time, datetime
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
from app.functions.booking_management import TicketSearch

        
        
async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[BookingTicket]:
    result = await db.execute(select(BookingTicket).where(BookingTicket.ticket_status == True)
                              .options(
                                  selectinload(BookingTicket.flight).selectinload(Flight.flight_route),
                                  selectinload(BookingTicket.ticket_class).selectinload(TicketClass.ticket_prices),
                                  selectinload(BookingTicket.employee)
                              ).offset(skip).limit(limit))
    
    return result.scalars().all()



async def search_by_filters(db: AsyncSession, filters: TicketSearch,skip: int = 0, limit: int = 100) -> List[BookingTicket]:
    
    query = (select(BookingTicket).join(BookingTicket.flight).join(BookingTicket.ticket_class).where(BookingTicket.ticket_status == True)
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
