from fastapi import FastAPI, HTTPException, APIRouter, Depends, status
from app.crud.phieudatcho_vemaybay import get_all_tickets, create_ticket, get_id,update_ticket, delete_ticket
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.phieudatcho_vemaybay import ThongTinHanhKhach, VeChuyenBay, PhieuDatChoVeMayBayInDB, PhieuDatChoVeMayBayCreate, PhieuDatChoVeMayBayUpdate
from typing import List
from datetime import date, datetime, timedelta
from app.deps import get_db


router = APIRouter()

@router.get("/", response_model=List[PhieuDatChoVeMayBayInDB])
async def read_all_tickets(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    try:
        tickets = await get_all_tickets(db, skip, limit)
        return tickets
    except Exception as e:
        raise HTTPException(status_code= 500, detail=str(e))


@router.post("/", response_model=PhieuDatChoVeMayBayInDB, status_code= status.HTTP_201_CREATED)
async def create_new_ticket(ticket: PhieuDatChoVeMayBayCreate, db: AsyncSession = Depends(get_db)):
    try: 
        new_ticket = await create_ticket(db,ticket)
        return new_ticket
    except Exception as e:
        raise HTTPException(status_code= 500, detail= str(e))
    
    
@router.put("/", response_model=PhieuDatChoVeMayBayInDB, status_code= status.HTTP_202_ACCEPTED)
async def update_info(id_pdc: str, obj_in : PhieuDatChoVeMayBayUpdate,db: AsyncSession = Depends(get_db)):
    db_obj = await get_id(db, id_pdc)
    
    if not db_obj:
        raise HTTPException(status_code= 404, detail= "Ticket not found")
    
    return await update_ticket(db, db_obj, obj_in)

@router.delete("/", response_model=PhieuDatChoVeMayBayInDB, status_code= status.HTTP_202_ACCEPTED)
async def delete_info(id_pdc: str,db: AsyncSession = Depends(get_db)):
    db_obj = await get_id(db ,id_pdc)
    
    if not db_obj:
        raise HTTPException(status_code= 404, detail= "Ticket not found")
    
    return await delete_ticket(db, db_obj)

