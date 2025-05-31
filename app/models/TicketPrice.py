from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class TicketPrice(Base):
    __tablename__ = "ticketprice"

    ticket_price_id = Column(String(50), primary_key=True)
    flight_route_id = Column(String(50), ForeignKey("flightroute.flight_route_id"), nullable=False)
    ticket_class_id = Column(String(50), ForeignKey("ticketclass.ticket_class_id"), nullable=False)
    price = Column(Integer, nullable=False)

    # Relationships
    flight_route = relationship("FlightRoute", back_populates="ticket_prices")
    ticket_class = relationship("TicketClass", back_populates="ticket_prices")
