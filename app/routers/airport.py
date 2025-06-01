from app.crud.airport import generate_airport_id, get_all_airports, update_airport, create_airport, delete_airport,get_id
from app.models.Airport import Airport
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional, List
from app.deps import get_db
from app.schemas.Airport import AirportInDB, AirportCreate, AirportUpdate
router = APIRouter()


@router.get("/", response_model=List[AirportInDB])
async def get_all(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    try:
        result = await get_all_airports(db, skip, limit)
        return result
    except Exception as e:
        raise HTTPException(status_code= 500, detail= str(e))
    
    


@router.post("/", response_model=AirportInDB, status_code= status.HTTP_201_CREATED)
async def create_new_airport(airport: AirportCreate, db: AsyncSession = Depends(get_db)):
    try: 
        new_airport = await create_airport(db,airport)
        return new_airport
    except Exception as e:
        raise HTTPException(status_code= 500, detail= str(e))
    
    
@router.put("/", response_model=AirportInDB, status_code= status.HTTP_202_ACCEPTED)
async def update_info(booking_airport_id: str, obj_in : AirportUpdate,db: AsyncSession = Depends(get_db)):
    db_obj = await get_id(db, booking_airport_id)
    
    if not db_obj:
        raise HTTPException(status_code= 404, detail= "Airport not found")
    
    return await update_airport(db, db_obj, obj_in)

@router.delete("/", response_model=AirportInDB, status_code= status.HTTP_202_ACCEPTED)
async def delete_info(booking_airport_id: str,db: AsyncSession = Depends(get_db)):
    db_obj = await get_id(db ,booking_airport_id)
    
    if not db_obj:
        raise HTTPException(status_code= 404, detail= "Airport not found")
    
    return await delete_airport(db, db_obj)
    
    
    
    
    