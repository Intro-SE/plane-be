from fastapi import APIRouter
from .employee import router as employee_router
from .auth import router as auth_router
from .booking_ticket import router as ticket_router
from .airport import router as airport_router
api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(employee_router, prefix="/employee", tags=["EmployeeAccount"])
api_router.include_router(ticket_router, prefix= "/tickets", tags=["Tickets"])
api_router.include_router(airport_router, prefix="/airports", tags= ["Aiports"])