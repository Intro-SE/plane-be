from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, joinedload
from app.models.base import Base

class TicketClass(Base):
    __tablename__ = "ticketclass"

    ticket_class_id = Column(String(50), primary_key=True)
    ticket_class_name = Column(String(50), nullable=False)

    # Relationships
    ticket_class_statistics = relationship("TicketClassStatistics", back_populates="ticket_class", lazy="joined")
    ticket_prices = relationship("TicketPrice", back_populates="ticket_class", lazy="joined")
    booking_tickets = relationship("BookingTicket", back_populates="ticket_class", lazy="joined")
