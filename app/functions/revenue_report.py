from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from datetime import datetime, date, time
from app.models.Flight import Flight
from app.models.BookingTicket import BookingTicket
from typing import Optional,List
from sqlalchemy import func, select, join,and_, or_
from sqlalchemy.orm import selectinload
from app.models.TicketClassStatistics import TicketClassStatistics


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
            month= "Tháng" + str(month),
            total_flight= total_flight,
            percertain=str(round(total_booked_seats/ total_seats * 100 if total_seats != 0 else 0)) + str("%"),
            revenue = revenue
        ))  
        
        
    return reports