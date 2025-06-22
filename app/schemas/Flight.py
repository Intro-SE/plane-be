from pydantic import BaseModel, Field
from datetime import datetime, time
from typing import List, Optional


class FlightRouteRef(BaseModel):
    flight_route_id: str
    departure_airport: str
    departure_address: str
    arrival_airport: str
    arrival_address: str
    class Config:
        from_attributes = True


class TicketClassStatisticsRef(BaseModel):
    ticket_class_id: str
    ticket_class_name: str
    total_seats: int
    available_seats: int
    booked_seats: int

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
    departure_time: time
    duration: int = Field(..., gt=0)
    total_seats: int = Field(..., gt=0)

    class Config:
        from_attributes = True


class FlightCreate(BaseModel):
    flight_route_id: str
    departure_date: datetime
    departure_time: time
    duration: int = Field(..., gt=0)
    total_seats: int = Field(..., gt=0)

    class Config:
        from_attributes = True


class FlightUpdate(BaseModel):
    departure_date: Optional[datetime] = None
    departure_time: Optional[time] = None
    duration: Optional[int] = Field(None, gt=0)
    total_seats: Optional[int] = Field(None, gt=0)

    class Config:
        from_attributes = True


class FlightInDB(FlightBase):
    flight_route: FlightRouteRef
    ticket_class_statistics: List[TicketClassStatisticsRef] = []

    @property
    def booked_seats(self) -> int:
        return sum(stat.booked_seats for stat in self.ticket_class_statistics)

    @property
    def available_seats(self) -> int:
        return sum(stat.available_seats for stat in self.ticket_class_statistics)

    @property
    def formatted_departure_datetime(self) -> str:
        return f"{self.departure_date.strftime('%d/%m/%Y')} {self.departure_time.strftime('%H:%M')}"

    class Config:
        from_attributes = True


class IntermediateStop(BaseModel):
    stop_number: int
    stop_name: str
    stop_time: int
    note: Optional[str]
    class Config:
        from_attributes = True


class SeatInformation(BaseModel):
    seat_type: List[str]
    seat_price: List[int]
    empty_type_seats: List[int]
    occupied_type_seats: List[int]
    empty_seats: int
    occupied_seats: int

    class Config:
        from_attributes = True


class FlightOut(BaseModel):
    flight_id: Optional[str] = None
    flight_route_id: Optional[str] = None
    departure_date: datetime
    total_seats: int
    departure_address: str
    departure_time: time
    departure_airport: str
    
    arrival_time: time
    arrival_airport: str
    arrival_address: str
    
    intermediate_stops: List[IntermediateStop]
    seat_information: SeatInformation

    class Config:
        from_attributes = True
