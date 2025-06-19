from sqlalchemy.ext.asyncio import AsyncSession
from app.functions.revenue_report import ReportOutputByMonth, report_by_month, ReportInput,ReportOutputByYear, report_by_year, FlightTransitOut, get_transit_airport

from app.deps import get_db

from typing import List
from fastapi import APIRouter, HTTPException, status, Depends



router = APIRouter()


@router.post("/report_month", response_model= List[ReportOutputByMonth])
async def report_month(input: ReportInput, db: AsyncSession = Depends(get_db)):
    try:
        result = await report_by_month(input, db)
        return result
    except Exception as e:
        raise HTTPException(status_code= 500, detail=str(e))
    
    
    
@router.post("/report_year", response_model= List[ReportOutputByYear])
async def report_year(input: ReportInput, db: AsyncSession = Depends(get_db)):
    try:
        result = await report_by_year(input, db)
        return result
    except Exception as e:
        raise HTTPException(status_code= 500, detail=str(e))
    
    
    
@router.get("/flight_detail", response_model= List[FlightTransitOut])
async def get_all_transit(db: AsyncSession = Depends(get_db)):
    try:
        result = await get_transit_airport(db)
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code= 500, detail= str(e))