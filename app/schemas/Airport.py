from pydantic import BaseModel, Field
from typing import List, Optional
from .FlightRoute import FlightRouteInDB
from .FlightDetail import FlightDetailInDB

class AirportBase(BaseModel):
    airport_id: str
    airport_name: str = Field(..., min_length=1, max_length=50)
    airport_address: str = Field(..., min_length=1, max_length=50)

    class Config:
        from_attributes = True

class AirportCreate(BaseModel):
    airport_name: str = Field(..., min_length=1, max_length=50)
    airport_address: str = Field(..., min_length=1, max_length=50)

    class Config:
        from_attributes = True

class AirportUpdate(BaseModel):
    airport_name: Optional[str] = Field(None, min_length=1, max_length=50)
    airport_address: Optional[str] = Field(None, min_length=1, max_length=50)

    class Config:
        from_attributes = True

class AirportInDB(AirportBase):
    flight_routes_from: List[FlightRouteInDB] = []
    flight_routes_to: List[FlightRouteInDB] = []
    transit_flight_details: List[FlightDetailInDB] = []

    @property
    def total_departures(self) -> int:
        return len(self.flight_routes_from)

    @property
    def total_arrivals(self) -> int:
        return len(self.flight_routes_to)

    @property
    def total_transits(self) -> int:
        return len(self.transit_flight_details)

    class Config:
        from_attributes = True