from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from datetime import datetime, date, time
from app.models.Flight import Flight
from app.models.BookingTicket import BookingTicket
from typing import Optional,List
from sqlalchemy import func, select, join,and_, or_
from sqlalchemy.orm import selectinload
from app.models.TicketClassStatistics import TicketClassStatistics
from app.models.FlightDetail import FlightDetail
import re
from app.models.Rules import Rules
from app.crud.airport import get_airport_name
from fastapi import HTTPException


class ReportInput(BaseModel):
    report_month: Optional[int] = None
    report_year: Optional[int] = None 
    
    
class ReportOutputByMonth(BaseModel):
    flight_id: Optional[str] = None
    last_occupied_seats: Optional[int] = None
    percertain: Optional[str] = None
    revenue: Optional[int] = None
    
    
    
class ReportOutputByYear(BaseModel):
    month: Optional[str] = None
    total_flight : Optional[int] = None
    percertain: Optional[str] = None
    revenue: Optional[int] = None
    
    
class FlightTransitOut(BaseModel):
    flight_route_id: Optional[str] = None
    transit_airport_name:Optional[str] = None
    stop_time: Optional[int] = None
    note: Optional[str] = None
    
async def report_by_month(report_input: ReportInput, db: AsyncSession)-> List[ReportOutputByMonth]:
    month = report_input.report_month
    year = report_input.report_year
    
    
    now = datetime.now()
    
    query = (select(Flight)
             .options(selectinload(Flight.ticket_class_statistics))
             .where(
                and_(
                    func.extract("month", Flight.flight_date) == month,
                    func.extract("year", Flight.flight_date) == year,
                    or_(
                        Flight.flight_date < now.date(),
                        and_(
                            Flight.flight_date == now.date(),
                            Flight.departure_time < now.time()
                        )
                    )
                )
             ))
    
    result = await db.execute(query)
    flights = result.scalars().all()
    
    reports = []
    
    
    for flight in flights:
        total_booked_seats = sum(stat.booked_seats for stat in flight.ticket_class_statistics)
        percertain = round(total_booked_seats / flight.flight_seat_count,2) if flight.flight_seat_count != 0 else 0
        
        
        price = (select(func.sum(BookingTicket.booking_price))
                 .where(
                     and_(                     
                        BookingTicket.flight_id == flight.flight_id)

                 ))
        
        revenue = await db.execute(price)
        
        revenue = revenue.scalar() or 0
        
        reports.append(ReportOutputByMonth(
            flight_id= flight.flight_id,
            last_occupied_seats= total_booked_seats,
            percertain= str(round(percertain * 100,2)) + "%",
            revenue= revenue
        ))
        
        
    return reports




async def report_by_year(report_input: ReportInput, db: AsyncSession) -> List[ReportOutputByYear]:
    year = report_input.report_year
    
    
    reports = []
    
    for month in range(1, 13):
        
        query = (
            select(Flight)
            .options(selectinload(Flight.ticket_class_statistics))
            .where(
                and_(
                    func.extract("month", Flight.flight_date) == month,
                    func.extract("year", Flight.flight_date) == year
                )
            )
        )
        
        flights = await db.execute(query)
        
        flights = flights.scalars().all()
        
        total_flight = len(flights)
        total_seats = 0
        revenue = 0
        total_booked_seats = 0
        for flight in flights:
            total_seats += flight.flight_seat_count
            total_booked_seats += sum(stat.booked_seats for stat in flight.ticket_class_statistics)
            query = (select(func.sum(BookingTicket.booking_price))
                     .where(
                         BookingTicket.flight_id == flight.flight_id
                     ))
            
            result = await db.execute(query)
            
            prices = result.scalar() or 0
            
            revenue += prices
            
            
        reports.append(ReportOutputByYear(
            month= "Tháng " + str(month),
            total_flight= total_flight,
            percertain=str(round(total_booked_seats/ total_seats * 100 if total_seats != 0 else 0)) + str("%"),
            revenue = revenue
        ))  
        
        
    return reports



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



    
    