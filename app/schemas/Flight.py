from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .FlightRoute import FlightRouteInDB
    from .TicketClassStatistics import TicketClassStatisticsInDB
    from .Employee import BookingTicketInDB


class FlightBase(BaseModel):
    flight_id: str
    route_id: str
    departure_date: datetime
    departure_time: datetime
    duration: int = Field(..., gt=0)
    total_seats: int = Field(..., gt=0)

    class Config:
        from_attributes = True


class FlightCreate(BaseModel):
    route_id: str
    departure_date: datetime
    departure_time: datetime
    duration: int = Field(..., gt=0)
    total_seats: int = Field(..., gt=0)

    class Config:
        from_attributes = True


class FlightUpdate(BaseModel):
    departure_date: Optional[datetime] = None
    departure_time: Optional[datetime] = None
    duration: Optional[int] = Field(None, gt=0)
    total_seats: Optional[int] = Field(None, gt=0)

    class Config:
        from_attributes = True


class FlightInDB(FlightBase):
    route: "FlightRouteInDB"
    ticket_class_statistics: List["TicketClassStatisticsInDB"] = []
    bookings: List["BookingTicketInDB"] = []

    @property
    def booked_tickets(self) -> int:
        return len(self.bookings)

    @property
    def available_tickets(self) -> int:
        return self.total_seats - self.booked_tickets

    @property
    def formatted_departure_datetime(self) -> str:
        return f"{self.departure_date.strftime('%d/%m/%Y')} {self.departure_time.strftime('%H:%M')}"

    class Config:
        from_attributes = True
