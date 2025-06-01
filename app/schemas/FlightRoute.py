from pydantic import BaseModel, Field
from typing import List, Optional

from datetime import time


class AirportRef(BaseModel):
    airport_id: str
    airport_name: str
    airport_address: str 
    class Config:
        from_attributes = True
        
        
class FlightRef(BaseModel):
    flight_id: str
    departure_time: time
    flight_duration: int
    class Config:
        from_attributes = True

class FlightDetailRef(BaseModel):
    flight_detail_id: str
    transit_airport_id: str
    stop_time: Optional[int] = None
    note: Optional[str] = None
    class Config:
        from_attributes = True

class TicketPriceRef(BaseModel):
    ticket_price_id: str
    ticket_class_id: str
    class Config:
        from_attributes = True
        
        
class FlightRouteBase(BaseModel):
    flight_route_id: str
    departure_airport_id: str
    arrival_airport_id: str
    class Config:
        from_attributes = True


class FlightRouteCreate(BaseModel):
    departure_airport_id: str
    arrival_airport_id: str

    class Config:
        from_attributes = True

class FlightRouteUpdate(BaseModel):
    departure_airport_id: Optional[str] = None
    arrival_airport_id: Optional[str] = None

    class Config:
        from_attributes = True

class FlightRouteInDB(FlightRouteBase):
    departure_airport: AirportRef
    arrival_airport: AirportRef
    flights: List[FlightRef] = []
    flight_details: List[FlightDetailRef] = []

    @property
    def total_flights(self) -> int:
        return len(self.flights)

    @property
    def total_transit_airports(self) -> int:
        return len(self.flight_details)

    @property
    def min_price(self) -> int:
        if not self.prices:
            return 0
        return min(price.price for price in self.prices)

    @property
    def max_price(self) -> int:
        if not self.prices:
            return 0
        return max(price.price for price in self.prices)


    class Config:
        from_attributes = True
