from pydantic import BaseModel, Field
from typing import List, Optional, TYPE_CHECKING

class TicketClassBase(BaseModel):
    ticket_class_id: str
    ticket_class_name: str = Field(..., min_length=1, max_length=50)

    class Config:
        from_attributes = True

class TicketClassCreate(BaseModel):
    ticket_class_name: str = Field(..., min_length=1, max_length=50)

    class Config:
        from_attributes = True

class TicketClassUpdate(BaseModel):
    ticket_class_name: Optional[str] = Field(None, min_length=1, max_length=50)

    class Config:
        from_attributes = True

class TicketClassInDB(TicketClassBase):
    ticket_class_statistics: List["TicketClassStatisticsInDB"] = []
    prices: List["TicketPriceInDB"] = []
    bookings: List["Booking_TicketInDB"] = []

    @property
    def total_booked_tickets(self) -> int:
        return len(self.bookings)

    @property
    def min_price(self) -> int:
        if not self.prices:
            return 0
        return min(price.price_amount for price in self.prices)

    @property
    def max_price(self) -> int:
        if not self.prices:
            return 0
        return max(price.price_amount for price in self.prices)

    class Config:
        from_attributes = True

if TYPE_CHECKING:
    from .TicketClassStatistics import TicketClassStatisticsInDB
    from .TicketPrice import TicketPriceInDB
    from .Employee import Booking_TicketInDB
