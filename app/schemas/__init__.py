from .Employee import (
    EmployeeBase,
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeInDB,
)

from .Booking_Ticket import (
    BookingTicketBase,
    BookingTicketCreate,
    BookingTicketUpdate,
    BookingTicketInDB,
)

from .TicketClassStatistics import TicketClassStatisticsInDB
from .TicketClass import TicketClassInDB
from .FlightRoute import FlightRouteInDB
from .Airport import AirportInDB, AirportCreate, AirportUpdate
from .Flight import FlightBase, FlightCreate, FlightInDB, FlightUpdate
from .TicketPrice import TicketPriceBase, TicketPriceCreate, TicketPriceInDB, TicketPriceUpdate
from .FlightDetail import FlightDetailBase, FlightDetailCreate, FlightDetailInDB, FlightDetailUpdate
FlightRouteInDB.model_rebuild()
BookingTicketInDB.model_rebuild()
TicketClassInDB.model_rebuild()
TicketClassStatisticsInDB.model_rebuild()
EmployeeInDB.model_rebuild()  
FlightDetailInDB.model_rebuild()
TicketPriceInDB.model_rebuild()
FlightInDB.model_rebuild()
AirportInDB.model_rebuild()