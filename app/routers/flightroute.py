from app.crud.flight_route import get_all_flightroutes, create_flightroute, update_flightroute, delete_flightroute,get_id
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.FlightRoute import FlightRoute
from app.schemas.FlightRoute import FlightRouteCreate, FlightRouteInDB, FlightRouteUpdate
from fastapi import APIRouter, HTTPException, status,Depends
from typing import List, Optional
from app.deps import get_db


router = APIRouter()




@router.get("/", response_model=List[FlightRouteInDB])
async def get_all(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    try:
        result = await get_all_flightroutes(db, skip, limit)
        return result
    except Exception as e:
        raise HTTPException(status_code= 500, detail=str(e))
    
@router.post("/")
    
    


@router.post("/", response_model=FlightRouteInDB, status_code= status.HTTP_201_CREATED)
async def create_new_flightroute(flightroute: FlightRouteCreate, db: AsyncSession = Depends(get_db)):
    try: 
        new_FlightRoute = await create_flightroute(db,flightroute)
        return new_FlightRoute
    except Exception as e:
        raise HTTPException(status_code= 500, detail= str(e))
    
    
@router.put("/", response_model=FlightRouteInDB, status_code= status.HTTP_202_ACCEPTED)
async def update_info(FlightRoute_id: str, obj_in : FlightRouteUpdate,db: AsyncSession = Depends(get_db)):
    db_obj = await get_id(db, FlightRoute_id)
    
    if not db_obj:
        raise HTTPException(status_code= 404, detail= "FlightRoute not found")
    
    return await update_flightroute(db, db_obj, obj_in)

@router.delete("/", response_model=FlightRouteInDB, status_code= status.HTTP_202_ACCEPTED)
async def delete_info(FlightRoute_id: str,db: AsyncSession = Depends(get_db)):
    db_obj = await get_id(db ,FlightRoute_id)
    
    if not db_obj:
        raise HTTPException(status_code= 404, detail= "FlightRoute not found")
    
    return await delete_flightroute(db, db_obj)
