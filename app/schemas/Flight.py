from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class FlightRouteRef(BaseModel):
    route_id: str
    departure_airport: str
    arrival_airport: str

    class Config:
        from_attributes = True


class TicketClassStatisticsRef(BaseModel):
    ticket_class_id: str
    ticket_class_name: str
    total_seats: int
    available_seats :int
    booked_seats : int
    class Config:
        from_attributes = True


class BookingTicketRef(BaseModel):
    booking_ticket_id: str
    passenger_name: str
    national_id: str
    booking_price: int
    ticket_status: bool

    class Config:
        from_attributes = True
        

class FlightBase(BaseModel):
    flight_id: str
    flight_route_id: str
    departure_date: datetime
    departure_time: datetime
    duration: int = Field(..., gt=0)
    total_seats: int = Field(..., gt=0)

    class Config:
        from_attributes = True


class FlightCreate(BaseModel):
    flight_route_id: str
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
    flight_route_id: FlightRouteRef
    ticket_class_statistics: List[TicketClassStatisticsRef] = []
    bookings: List[BookingTicketRef] = []

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
