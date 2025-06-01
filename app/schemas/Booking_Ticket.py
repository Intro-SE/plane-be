from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional, TYPE_CHECKING
from datetime import time

class FlightRef(BaseModel):
    flight_id: str
    flight_route_id: str
    flight_date: date
    departure_time: time
    flight_duration: int
    flight_seat_count: int

    class Config:
        from_attributes = True

class TicketClassRef(BaseModel):
    ticket_class_id: str
    ticket_class_name: str

    class Config:
        from_attributes = True

class EmployeeRef(BaseModel):
    employee_id: str
    employee_name: str
    phone_number: str

    class Config:
        from_attributes = True

class BookingTicketBase(BaseModel):
    booking_ticket_id: str
    flight_id: str
    passenger_name: str = Field(..., min_length=1, max_length=50)
    national_id: str = Field(..., pattern=r'^(\d{9}|\d{12})$')
    gender: str = Field(..., pattern=r'^(Nam|Nữ)$')
    phone_number: str = Field(..., pattern=r'^\d{10}$')
    ticket_class_id: str
    booking_price: int = Field(..., gt=0)
    booking_date: date
    ticket_status: bool
    employee_id: str

    class Config:
        from_attributes = True
        json_encoders = {
            date: lambda v: v.strftime("%Y-%m-%d")
        }

class BookingTicketCreate(BaseModel):
    flight_id: str
    passenger_name: str = Field(..., min_length=1, max_length=50)
    national_id: str = Field(..., pattern=r'^(\d{9}|\d{12})$')
    gender: str = Field(..., pattern=r'^(Nam|Nữ)$')
    phone_number: str = Field(..., pattern=r'^\d{10}$')
    ticket_class_id: str
    booking_price: int = Field(..., gt=0)
    ticket_status: bool = Field(default=False)
    employee_id: str

    class Config:
        from_attributes = True

class BookingTicketUpdate(BaseModel):
    passenger_name: Optional[str] = Field(None, min_length=1, max_length=50)
    national_id: Optional[str] = Field(None, pattern=r'^(\d{9}|\d{12})$')
    gender: Optional[str] = Field(None, pattern=r'^(Nam|Nữ)$')
    phone_number: Optional[str] = Field(None, pattern=r'^\d{10}$')
    ticket_class_id: Optional[str] = None
    booking_price: Optional[int] = Field(None, gt=0)
    ticket_status: Optional[bool] = None

    class Config:
        from_attributes = True

class BookingTicketInDB(BookingTicketBase):
    flight: Optional[FlightRef] = None
    ticket_class: Optional[TicketClassRef] = None
    employee: Optional[EmployeeRef] = None

    @property
    def ticket_status_display(self) -> str:
        return "Đã xuất vé" if self.ticket_status else "Chưa xuất vé"

    @property
    def booking_date_format(self) -> str:
        return self.booking_date.strftime("%d/%m/%Y")

    @property
    def booking_price_format(self) -> str:
        return f"{self.booking_price:,} VNĐ"

    class Config:
        from_attributes = True

class PassengerInfo(BaseModel):
    gender: str
    national_id: str
    passenger_name: str
    phone_number: str

class FlightTicketInfo(BaseModel):
    booking_ticket_id: str
    flight_id: str
    ticket_class_name: str

    departure_airport_name: str
    departure_airport_id: str
    flight_date: date
    departure_time: time

    arrival_airport_name: str
    arrival_airport_id: str
    arrival_date: str
    arrival_time: str

    passenger_info: PassengerInfo
    booking_price: int

    class Config:
        from_attributes = True
    
