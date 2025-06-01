from pydantic import BaseModel, Field
from typing import Optional, TYPE_CHECKING

class FlightDetailBase(BaseModel):
    flight_detail_id: str
    flight_route_id: str
    transit_airport_id: str
    stop_time: int = Field(..., gt=0)
    note: Optional[str] = None

    class Config:
        from_attributes = True

class FlightDetailCreate(BaseModel):
    flight_route_id: str
    transit_airport_id: str
    stop_time: int = Field(..., gt=0)
    note: Optional[str] = None

    class Config:
        from_attributes = True

class FlightDetailUpdate(BaseModel):
    stop_time: Optional[int] = Field(None, gt=0)
    note: Optional[str] = None

    class Config:
        from_attributes = True

class FlightDetailInDB(FlightDetailBase):
    route: "FlightRouteInDB"
    transit_airport: "AirportInDB"

    @property
    def stop_time_format(self) -> str:
        return f"{self.stop_time} phút"

    class Config:
        from_attributes = True

if TYPE_CHECKING:
    from .FlightRoute import FlightRouteInDB
    from .Airport import AirportInDB
