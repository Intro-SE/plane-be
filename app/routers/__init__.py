from fastapi import APIRouter
from .employee import router as employee_router
from .auth import router as auth_router
from .booking_ticket import router as ticket_router
from .airport import router as airport_router
from .flightroute import router as flightroute_router
from .flight import router as flight_router
from .flight_lookup import router as flights
from .flight_management import router as flights_management
from .booking_management import router as bookings_management
from .flight_ticket_management import router as flight_tickets_management
api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(flights, prefix="/flight", tags=["Flight"])
api_router.include_router(flights_management,prefix= "/flight_management", tags= ["Flight Management"])
api_router.include_router(bookings_management,prefix= "/booking_management", tags= ["Booking Management"])
api_router.include_router(flight_tickets_management,prefix= "/flight_ticket_management", tags= ["Flight Ticket Management"])


api_router.include_router(employee_router, prefix="/employee_crud", tags=["EmployeeAccount_CRUD"])
api_router.include_router(flight_router, prefix="/flights_crud", tags=["Flight_CRUD"])
api_router.include_router(ticket_router, prefix= "/tickets_crud", tags=["Tickets_CRUD"])
api_router.include_router(airport_router, prefix="/airports_crud", tags= ["Aiports_CRUD"])
api_router.include_router(flightroute_router, prefix="/flightroutes_crud", tags= ["FlightRoute_CRUD"])