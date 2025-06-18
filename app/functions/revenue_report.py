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
    percertain: Optional[float] = None
    revenue: Optional[int] = None
    
    
    
class ReportOutputByYear(BaseModel):
    month: Optional[int] = None
    total_flight : Optional[int] = None
    percertain: Optional[int] = None
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
            percertain= percertain,
            revenue= revenue
        ))
        
        
    return reports