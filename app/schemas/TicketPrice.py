from pydantic import BaseModel, Field
from typing import Optional, TYPE_CHECKING

class TicketPriceBase(BaseModel):
    ticket_price_id: str
    flight_route_id: str
    ticket_class_id: str
    price: int = Field(..., gt=0)

    class Config:
        from_attributes = True

class TicketPriceCreate(BaseModel):
    flight_route_id: str
    ticket_class_id: str
    price: int = Field(..., gt=0)

    class Config:
        from_attributes = True

class TicketPriceUpdate(BaseModel):
    price: Optional[int] = Field(None, gt=0)

    class Config:
        from_attributes = True

class TicketPriceInDB(TicketPriceBase):
    flight_route: "FlightRouteInDB"
    ticket_class: "TicketClassInDB"

    @property
    def price_formatted(self) -> str:
        return f"{self.price:,} VNĐ"

    class Config:
        from_attributes = True

if TYPE_CHECKING:
    from .FlightRoute import FlightRouteInDB
    from .TicketClass import TicketClassInDB