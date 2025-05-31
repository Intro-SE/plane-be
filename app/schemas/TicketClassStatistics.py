from pydantic import BaseModel, Field
from typing import Optional, TYPE_CHECKING

class TicketClassStatisticsBase(BaseModel):
    ticket_class_statistics_id: str
    flight_id: str
    ticket_class_id: str
    total_seats: int = Field(..., gt=0)
    available_seats: int = Field(..., ge=0)
    booked_seats: int = Field(..., ge=0)

    class Config:
        from_attributes = True

class TicketClassStatisticsCreate(BaseModel):
    flight_id: str
    ticket_class_id: str
    total_seats: int = Field(..., gt=0)
    available_seats: int = Field(..., ge=0)
    booked_seats: int = Field(..., ge=0)

    class Config:
        from_attributes = True

class TicketClassStatisticsUpdate(BaseModel):
    total_seats: Optional[int] = Field(None, gt=0)
    available_seats: Optional[int] = Field(None, ge=0)
    booked_seats: Optional[int] = Field(None, ge=0)

    class Config:
        from_attributes = True

class TicketClassStatisticsInDB(TicketClassStatisticsBase):
    flight: "FlightInDB"
    ticket_class: "TicketClassInDB"

    @property
    def booking_rate(self) -> float:
        if self.total_seats == 0:
            return 0.0
        return (self.booked_seats / self.total_seats) * 100

    @property
    def booking_rate_formatted(self) -> str:
        return f"{self.booking_rate:.1f}%"

    class Config:
        from_attributes = True

if TYPE_CHECKING:
    from .Flight import FlightInDB
    from .TicketClass import TicketClassInDB
