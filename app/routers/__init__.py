from fastapi import APIRouter
from .taikhoannhanvien import router as employee_router
from .auth import router as auth_router

api_router = APIRouter()

api_router.include_router(employee_router, prefix="/employee", tags=["EmployeeAccount"])
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
