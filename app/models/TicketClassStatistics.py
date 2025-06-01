from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class TicketClassStatistics(Base):
    __tablename__ = "ticketclassstatistics"

    ticket_class_statistics_id = Column(String(50), primary_key=True)
    flight_id = Column(String(50), ForeignKey("flight.flight_id"), nullable=False)
    ticket_class_id = Column(String(50), ForeignKey("ticketclass.ticket_class_id"), nullable=False)
    total_seats = Column(Integer, nullable=False)
    available_seats = Column(Integer, nullable=False)
    booked_seats = Column(Integer, nullable=False)

    # Relationships
    flight = relationship("Flight", back_populates="ticket_class_statistics")
    ticket_class = relationship("TicketClass", back_populates="ticket_class_statistics")
