from pydantic import BaseModel, Field
from typing import List, Optional

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Airport import AirportInDB
    from .Flight import FlightInDB
    from .FlightDetail import FlightDetailInDB
    from .TicketPrice import TicketPriceInDB


class FlightRouteBase(BaseModel):
    route_id: str
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
    departure_airport: "AirportInDB"
    arrival_airport: "AirportInDB"
    flights: List["FlightInDB"] = []
    flight_details: List["FlightDetailInDB"] = []
    prices: List["TicketPriceInDB"] = []

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
        return min(price.giatien for price in self.prices)

    @property
    def max_price(self) -> int:
        if not self.prices:
            return 0
        return max(price.giatien for price in self.prices)

    class Config:
        from_attributes = True
