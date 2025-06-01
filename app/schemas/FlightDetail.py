from pydantic import BaseModel, Field
from typing import Optional, TYPE_CHECKING

class FlightDetailBase(BaseModel):
    flight_detail_id: str
    route_id: str
    transit_airport_id: str
    transit_duration: int = Field(..., gt=0)
    note: Optional[str] = None

    class Config:
        from_attributes = True

class FlightDetailCreate(BaseModel):
    route_id: str
    transit_airport_id: str
    transit_duration: int = Field(..., gt=0)
    note: Optional[str] = None

    class Config:
        from_attributes = True

class FlightDetailUpdate(BaseModel):
    transit_duration: Optional[int] = Field(None, gt=0)
    note: Optional[str] = None

    class Config:
        from_attributes = True

class FlightDetailInDB(FlightDetailBase):
    route: "FlightRouteInDB"
    transit_airport: "AirportInDB"

    @property
    def transit_duration_format(self) -> str:
        return f"{self.transit_duration} phút"

    class Config:
        from_attributes = True

if TYPE_CHECKING:
    from .FlightRoute import FlightRouteInDB
    from .Airport import AirportInDB
