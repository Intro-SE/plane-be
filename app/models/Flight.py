from sqlalchemy import Column, String, Date, Time, Integer, ForeignKey
from sqlalchemy.orm import relationship, joinedload
from app.models.base import Base

from datetime import datetime

class Flight(Base):
    __tablename__ = "flight"

    flight_id = Column(String(50), primary_key=True)
    flight_route_id = Column(String(50), ForeignKey("flightroute.flight_route_id"), nullable=False)
    flight_date = Column(Date, nullable=False)
    departure_time = Column(Time, nullable=False)
    flight_duration = Column(Integer, nullable=False)
    flight_seat_count = Column(Integer, nullable=False)

    # Relationships
    flight_route = relationship("FlightRoute", back_populates="flights", lazy="selectin")
    ticket_class_statistics = relationship("TicketClassStatistics", back_populates="flight", lazy="selectin", cascade= "all, delete-orphan")
    booking_tickets = relationship("BookingTicket", back_populates="flight", lazy="selectin", cascade= "all, delete-orphan")
    
    
    @property
    def is_expired(self) -> bool:
        now = datetime.now()
        
        return (
            self.flight_date < now.date()
            or (self.flight_date == now.date() and self.departure_time < now.time())
        )