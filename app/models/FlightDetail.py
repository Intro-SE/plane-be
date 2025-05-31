from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class FlightDetail(Base):
    __tablename__ = "flightdetail"

    flight_detail_id = Column(String(50), primary_key=True)
    flight_route_id = Column(String(50), ForeignKey("flightroute.flight_route_id"), nullable=False)
    transit_airport_id = Column(String(50), ForeignKey("airport.airport_id"), nullable=False)
    stop_time = Column(Integer, nullable=False)
    note = Column(String(200))

    # Relationships
    flight_route = relationship("FlightRoute", back_populates="flightdetails")
    transit_airport = relationship("Airport")