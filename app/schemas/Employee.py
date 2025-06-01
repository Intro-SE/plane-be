from __future__ import annotations
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.Booking_Ticket import BookingTicketInDB  

class EmployeeBase(BaseModel):
    employee_id: str
    employee_username: str = Field(..., min_length=3, max_length=200)
    employee_password: str = Field(..., min_length=3, max_length=200)
    employee_name: str = Field(..., min_length=1, max_length=50)
    national_id: str = Field(..., pattern=r'^\d{9}$|^\d{12}$')
    phone_number: str = Field(..., pattern=r'^\d{10}$')
    gender: str | None = Field(None, pattern=r'^(Nam|Nữ)$')
    created_date: datetime

    class Config:
        from_attributes = True

class EmployeeCreate(BaseModel):
    employee_username: str = Field(..., min_length=3, max_length=200)
    employee_password: str = Field(..., min_length=3, max_length=200)
    employee_name: str = Field(..., min_length=1, max_length=50)
    national_id: str = Field(..., pattern=r'^\d{9}$|^\d{12}$')
    phone_number: str = Field(..., pattern=r'^\d{10}$')
    gender: str | None = Field(None, pattern=r'^(Nam|Nữ)$')
    created_date: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True

class EmployeeUpdate(BaseModel):
    employee_username: str | None = Field(None, min_length=3, max_length=200)
    employee_password: str | None = Field(None, min_length=3, max_length=200)
    employee_name: str | None = Field(None, min_length=1, max_length=50)
    national_id: str | None = Field(None, pattern=r'^\d{9}$|^\d{12}$')
    phone_number: str | None = Field(None, pattern=r'^\d{10}$')
    gender: str | None = Field(None, pattern=r'^(Nam|Nữ)$')

    class Config:
        from_attributes = True

class EmployeeInDB(EmployeeBase):
    booking_tickets: List["BookingTicketInDB"] = []

    @property
    def booking_count(self) -> int:
        return len(self.booking_tickets)

    @property
    def created_date_format(self) -> str:
        return self.created_date.strftime("%d/%m/%Y %H:%M")

    @property
    def status(self) -> str:
        return "Đang hoạt động" if self.booking_count > 0 else "Chưa hoạt động"

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }
