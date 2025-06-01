from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class FlightRoute(Base):
    __tablename__ = "flightroute"

    flight_route_id = Column(String(50), primary_key=True)
    departure_airport_id = Column(String(50), ForeignKey("airport.airport_id"), nullable=False)
    arrival_airport_id = Column(String(50), ForeignKey("airport.airport_id"), nullable=False)

    # Relationships
    departure_airport = relationship("Airport", foreign_keys=[departure_airport_id], lazy="selectin")
    arrival_airport = relationship("Airport", foreign_keys=[arrival_airport_id], lazy="selectin")
    flights = relationship("Flight", back_populates="flight_route", lazy="selectin")
    flight_details = relationship("FlightDetail", back_populates="flight_route", lazy="selectin")
    ticket_prices = relationship("TicketPrice", back_populates="flight_route", lazy="selectin")